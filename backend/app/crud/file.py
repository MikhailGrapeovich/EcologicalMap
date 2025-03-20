from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import File, User, Pollution
async def create_file(session: AsyncSession,owner:User,pollution: Pollution, file:UploadFile):
    db_obj = File(file=file, owner_id=owner.id, owner=owner, pollution=pollution, pollution_id=pollution.id)
    session.add(db_obj)
    return db_obj