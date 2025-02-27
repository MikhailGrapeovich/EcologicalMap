from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int | None]
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    age: Mapped[Optional[int]]
    hashed_password: Mapped[str]
    # Permissions
    is_superuser: Mapped[bool] = mapped_column(server_default="false")
    is_active: Mapped[bool] = mapped_column(server_default="true")
    files: Mapped[List["File"]] = relationship("File", foreign_keys="[File.owner_id]", uselist=True)
