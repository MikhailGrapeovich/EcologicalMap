from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.schemas.pollution as schemas_pollution
from app.models import Pollution
from app.utils.auth import get_password_hash




async def get_pollution(session: AsyncSession, pollution_id: int) -> Pollution:
    pollution = await session.get(Pollution, pollution_id)
    if pollution is None:
        raise HTTPException(404, "Pollution not found.")
    return pollution


async def create_pollution(session: AsyncSession, pollution_in: schemas_pollution.PollutionCreate, owner_id: int)->Pollution:
    pollution = Pollution(**pollution_in.model_dump(),
                          owner_id=owner_id)
    session.add(pollution)
    return pollution


async def delete_pollution(session: AsyncSession, pollution_id: int) -> None:
    await session.delete(await get_pollution(session, pollution_id))


async def update_pollution(session: AsyncSession, pollution_id: int, pollution_in: schemas_pollution.PollutionUpdate) -> Pollution:
    pollution = await get_pollution(session, pollution_id)
    for k, v in pollution_in.model_dump(exclude_unset=True).items():
        setattr(pollution, k, v)
    return pollution

