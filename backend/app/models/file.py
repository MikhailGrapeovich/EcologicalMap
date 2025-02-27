from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_storages import FileSystemStorage
from sqlalchemy import Column, ForeignKey
from fastapi_storages.integrations.sqlalchemy import FileType as _FileType
from typing import Any
from app.config import settings


class FileType(_FileType):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(storage=FileSystemStorage(path=settings.MEDIA_ROOT / "files"), *args, **kwargs)
class File(BaseModel):
    __tablename__="file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file = Column(FileType())
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    owner: Mapped["User"] = relationship("User",foreign_keys=owner_id)