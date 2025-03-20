from typing import List

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped

class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    age: int
    # Permissions
    is_superuser: bool
    is_active: bool


class UserSimple(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserPublic(UserSimple):
    accepted_pollutions: List["PollutionSimple"] = []
    pollutions: List["PollutionSimple"] = []
    points: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...


class UserUpdateMe(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

from app.schemas.pollution import PollutionSimple
UserBase.update_forward_refs()