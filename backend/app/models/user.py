from sqlalchemy import Table, Column, Integer, ForeignKey

from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

user_pollution_association = Table(
    "user_pollution",  # Имя таблицы
    BaseModel.metadata,  # Метаданные
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True), # Внешний ключ на User
    Column("pollution_id", Integer, ForeignKey("pollution.id"), primary_key=True), # Внешний ключ на Pollution
)


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
    pollutions: Mapped[List["Pollution"]] = relationship("Pollution", foreign_keys="[Pollution.owner_id]", uselist=True, back_populates="owner", lazy="selectin")
    accepted_pollutions: Mapped[List["Pollution"]] = relationship(secondary=user_pollution_association, back_populates="performers", lazy="selectin") # Связь через ассоциативную таблицу
    points: Mapped[int] = mapped_column(Integer, default="500", server_default="500")
