
from urllib.parse import urljoin
from pathlib import Path
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
    pollution_id: Mapped[int] = mapped_column(ForeignKey("pollution.id"), nullable=False)
    pollution: Mapped["Pollution"] = relationship("Pollution", foreign_keys=pollution_id, back_populates="images")

    @property
    def file_name(self) -> str | None:
        if self.file is None:
            return
        if hasattr(self.file, "name"):
            return str(self.file.name)
        if hasattr(self.file, "filename"):
            return str(self.file.filename)

    @property
    def url(self) -> str:
        """Generates the URL for the file."""
        return f"{settings.PROTO}://{settings.HOST}/files/{self.file_name}"  # file_path already includes the relative path

