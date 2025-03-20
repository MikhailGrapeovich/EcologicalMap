from app.models.user import user_pollution_association
from app.enums import TypePollutionEnum, StagePollutionEnum
from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi import File
from typing import List
from app.enums import DifficultyLevelEnum
from app.models.base import BaseModel


class Pollution(BaseModel):
    __tablename__ = "pollution"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    type: Mapped[str] = mapped_column(default=TypePollutionEnum.trash)
    stage: Mapped[str] = mapped_column(default=StagePollutionEnum.DETECTED,
                                       server_default=f"{StagePollutionEnum.DETECTED}")
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship("User", foreign_keys=owner_id, back_populates="pollutions")
    performers: Mapped[List["User"]] = relationship(secondary=user_pollution_association,
                                                    back_populates="accepted_pollutions",
                                                    lazy="selectin", uselist=True)  # Связь через ассоциативную таблицу
    images: Mapped[List["File"]] = relationship("File", lazy="selectin", foreign_keys="[File.pollution_id]",
                                                uselist=True, back_populates="pollution", cascade="all, delete")
    points: Mapped[int] = mapped_column(Integer, default="500", server_default="500")
    difficulty: Mapped[str] = mapped_column(default=f"{DifficultyLevelEnum.MEDIUM.value}", server_default=f"{DifficultyLevelEnum.MEDIUM.value}")
