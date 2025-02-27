import asyncio
from app.config import settings
from app.database import get_db_session
from app.models.user import User
from app.utils.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
async def init_db(session: AsyncSession):
    super_user = User(username=settings.FIRST_SUPERUSER,
                      email=settings.FIRST_SUPERUSER,
                      first_name="admin",
                      last_name="super",
                      age=666,
                      hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASS),
                      is_superuser=True,
                      is_active=True
                      )
    session.add(instance=super_user)
    await session.commit()
    await session.refresh(super_user)
    print("Superuser created")

async def main():
    print("Creating initial data...")
    async for session in get_db_session():
        await init_db(session)
    print("Initial data created")
if __name__=="__main__":
    asyncio.run(main())
