
from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    file_name: str | None = None
    owner_id: int  | None = None
    pollution_id: int  | None = None

    url: str  | None = None


class FilePublic(FileBase):
    id: int
    model_config = ConfigDict(from_attributes=True) #  Добавляем ConfigDict и в FilePublic