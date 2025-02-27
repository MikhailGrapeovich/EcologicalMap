from fastapi import APIRouter, Depends
import app.crud.user as crud_user
from app.api.dependencies.db import SessionDep
import app.schemas.user as schemas_user
import app.schemas.message as text
from app.api.dependencies.auth import CurrentUser,CurrentSuperUser, get_current_superuser
from typing import Any
from app.schemas.message import Message
from app.utils.auth import verify_password, get_password_hash
from app.exeptions import IncorrectPasswordException, SamePasswordException
router = APIRouter()
@router.get("/{user_id}", dependencies=[Depends(get_current_superuser)],
            response_model=schemas_user.UserPublic)
async def read_user(user_id: int, session: SessionDep):
    return await crud_user.get_user(session, user_id)

@router.post("/",
             response_model=schemas_user.UserPublic,
             dependencies=[Depends(get_current_superuser)],)
async def create_user(session: SessionDep, user_in: schemas_user.UserCreate):
    await crud_user.check_user_unique(session, user_in)
    user = await crud_user.create_user(session, user_in)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/{user_id}",
               dependencies=[Depends(get_current_superuser)],
               response_model=text.Message)
async def delete_user(user_id: int, session: SessionDep):
    await crud_user.delete_user(session, user_id)
    await session.commit()
    return text.Message(text="User deleted")

@router.patch("/{user_id}",
              response_model=schemas_user.UserPublic,
              dependencies=[Depends(get_current_superuser)],)
async def update_user(user_id: int, session: SessionDep, user_in: schemas_user.UserUpdate | schemas_user.UserUpdateMe):
    await crud_user.check_user_unique(session, user_in, exclude_id=user_id)
    user = await crud_user.update_user(session, user_id, user_in)
    await session.commit()
    await session.refresh(user)
    return user

@router.get("/me",            response_model=schemas_user.UserPublic)
async def read_user_me( session: SessionDep, current_user: CurrentUser):
    return await crud_user.get_user(session, current_user.id)


@router.patch("/me",
              response_model=schemas_user.UserPublic,)
async def update_user_me(current_user:CurrentUser, session: SessionDep, user_in: schemas_user.UserUpdateMe):
    await crud_user.check_user_unique(session, user_in, exclude_id=current_user.id)
    user = await crud_user.update_user(session, current_user.id, user_in)
    await session.commit()
    await session.refresh(user)
    return user

@router.patch("/me/password", response_model=Message)
async def update_password_me(
    *, session: SessionDep, body: schemas_user.UpdatePassword, current_user: CurrentUser
) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise IncorrectPasswordException
    if body.current_password == body.new_password:
        raise SamePasswordException
    current_user.hashed_password = get_password_hash(body.new_password)
    await session.commit()
    return Message(text="Password updated successfully.")