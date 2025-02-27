from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.schemas.user as schemas_user
from app.models import User
from app.crud.utils import is_object_unique
from app.utils.auth import get_password_hash
from sqlalchemy import select
from app.utils.auth import verify_password


async def is_user_unique(session: AsyncSession, user_in: schemas_user.UserBase | schemas_user.UserUpdateMe,
                         exclude_id: int | None = None) -> bool:
    return await is_object_unique(session, User, user_in, ("username", "email"), exclude_id)


async def check_user_unique(session: AsyncSession, user_in: schemas_user.UserBase | schemas_user.UserUpdateMe,
                            exclude_id: int | None = None) -> None:
    if not await is_user_unique(session, user_in, exclude_id):
        raise HTTPException(400, "User with this email or username already exists.")


async def get_user(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(404, "User not found.")
    return user


async def create_user(session: AsyncSession, user_in: schemas_user.UserCreate)->User:
    user = User(**user_in.model_dump(exclude={"password"}),
                hashed_password=get_password_hash(user_in.password))
    session.add(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    await session.delete(await get_user(session, user_id))


async def update_user(session: AsyncSession, user_id: int, user_in: schemas_user.UserUpdate | schemas_user.UserUpdateMe) -> User:
    user = await get_user(session, user_id)
    for k, v in user_in.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    return user

async def get_user_by_unique_field(session: AsyncSession, field: str, value: str) -> User | None:
    return (await session.scalars(select(User).where(getattr(User, field) == value))).one_or_none()

async def get_user_by_mail(session: AsyncSession, email: str) -> User | None:
    return await get_user_by_unique_field(session, "email", email)

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    return await get_user_by_unique_field(session, "username", username)
async def authenticate(session: AsyncSession, username: str, password: str) -> User | None:
    user = await get_user_by_username(session, username)
    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
