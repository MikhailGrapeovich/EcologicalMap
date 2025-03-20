from fastapi import APIRouter, Depends, Query, Form, UploadFile
from sqlalchemy.exc import SQLAlchemyError

import app.crud.pollution as crud_pollution
from app.api.dependencies.db import SessionDep
import app.schemas.pollution as schemas_pollution
from app.schemas.pollution import PollutionPublic
import app.schemas.message as text
from app.api.dependencies.auth import CurrentUser, CurrentSuperUser, get_current_superuser
from typing import Any, Annotated, Optional, List, Union
from app.database import get_db_session
from app.models import User
from app.schemas.message import Message
from app.utils.auth import verify_password, get_password_hash
from app.exeptions import IncorrectPasswordException, SamePasswordException, ErrorNoPrivilegesException
from sqlalchemy import select
from app.models.pollution import Pollution
from app.crud.file import create_file
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.enums import StagePollutionEnum

router = APIRouter()


@router.get("/",
            response_model=list[PollutionPublic])
async def read_all_pollutions(session: SessionDep,
                              skip: Annotated[int, Query(qe=0, )] = 0,
                              limit: Annotated[int | None, Query(qt=0, )] = None):
    statement = select(Pollution).offset(skip)
    if limit:
        statement = statement.limit(limit)
    return list((await session.scalars(statement)).all())


@router.get("/{pollution_id}",
            response_model=PollutionPublic)
async def read_pollution(pollution_id: int, session: SessionDep):
    return await crud_pollution.get_pollution(session, pollution_id)

"""
@router.post("/",
             response_model=schemas_pollution.PollutionPublic,
             )
async def create_pollution(session: SessionDep, pollution_in: schemas_pollution.PollutionCreate,
                           current_user: CurrentUser):
    pollution = await crud_pollution.create_pollution(session, pollution_in, current_user.id)
    await session.commit()
    await session.refresh(pollution)
    return pollution
"""

@router.delete("/{pollution_id}",
               response_model=text.Message)
async def delete_pollution(pollution_id: int, session: SessionDep, current_user: CurrentUser):
    if (await crud_pollution.get_pollution(session,
                                           pollution_id)).owner_id != current_user.id and not current_user.is_superuser:
        raise ErrorNoPrivilegesException
    await crud_pollution.delete_pollution(session, pollution_id)
    await session.commit()
    return text.Message(text="Pollution deleted")


@router.patch("/{pollution_id}",
              response_model=PollutionPublic,
              )
async def update_pollution(pollution_id: int, session: SessionDep, pollution_in: schemas_pollution.PollutionUpdate,
                           current_user: CurrentUser):
    if (await crud_pollution.get_pollution(session,
                                           pollution_id)).owner_id != current_user.id and not current_user.is_superuser:
        raise ErrorNoPrivilegesException
    pollution = await crud_pollution.update_pollution(session, pollution_id, pollution_in)
    await session.commit()
    await session.refresh(pollution)
    return pollution

@router.post("/",
              response_model=PollutionPublic,
              )
async def create_pollution(session: SessionDep,
                         current_user: CurrentUser,
                         longitude: Optional[Union[float]] = Form(None),
                         latitude: Optional[Union[float]] = Form(None),
                         type: Optional[Union[str]] = Form(None),
                         description: Optional[Union[str]] = Form(None),
                         points: Optional[Union[int]] = Form(None),
                         files: List[UploadFile] = []):
    pollution_data = {"longitude":longitude,
                      "latitude":latitude,
                      "type":type,
                      "description":description,
                      "points":points,
                      "difficulty": schemas_pollution.PollutionCreate.calculate_difficulty(points)}
    pollution_in = schemas_pollution.PollutionCreate(**pollution_data)
    pollution = await crud_pollution.create_pollution(session, pollution_in, current_user.id)
    await session.commit()
    if files:
        for file in files:
            await create_file(session, current_user, pollution, file)
            await session.commit()
    await session.refresh(pollution)
    return pollution


# ---- Пример API-метода для обновления статуса задания ----
@router.put("/{pollution_id}/resolve", response_model=PollutionPublic, summary="Mark a pollution as resolved")
async def resolve_pollution(pollution_id: int, session: SessionDep):
    """Marks a pollution as resolved and distributes points to performers."""
    db_pollution = await session.execute(select(Pollution).where(Pollution.id == pollution_id)).scalar_one_or_none()
    if not db_pollution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pollution not found")

    if db_pollution.stage == StagePollutionEnum.RESOLVED:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pollution is already resolved")

    try:
        db_pollution.stage = StagePollutionEnum.RESOLVED

        performers = db_pollution.performers
        num_performers = len(performers)

        if num_performers > 0:
            points_per_performer = db_pollution.points // num_performers
            remainder = db_pollution.points % num_performers

            for i, performer in enumerate(performers):
                user = session.query(User).filter(User.id == performer.id).first()
                user.points += points_per_performer

                if i < remainder:
                    user.points += 1

                session.add(user)

        await session.commit() #применяем изменения только если все прошло успешно

    except SQLAlchemyError as e: #откатываем изменения в случае ошибки
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")

    finally:
        await session.refresh(db_pollution)

    return db_pollution

"""
@router.post("/pollutions/{pollution_id}/add_performers", response_model=PollutionPublic, summary="Add performers to a pollution")
async def add_performers(pollution_id: int, user_ids: List[int], db: Session = Depends(get_db_session)):
    #Adds a list of users as performers to a pollution.
    db_pollution = db.query(Pollution).filter(Pollution.id == pollution_id).first()
    if not db_pollution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pollution not found")
    for user_id in user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")

        if user not in db_pollution.performers: # Проверяем, что пользователь еще не в списке
            db_pollution.performers.append(user)

    db.add(db_pollution)
    await db.commit()
    await db.refresh(db_pollution)
    
    return db_pollution
"""