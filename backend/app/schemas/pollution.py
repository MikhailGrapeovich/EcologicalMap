from typing import List, Optional
from app.enums import TypePollutionEnum, StagePollutionEnum
from pydantic import BaseModel, ConfigDict, model_validator, Field
from app.schemas.file import FilePublic
from app.utils.decoration import partial_model




class PollutionBase(BaseModel):
    description: str
    type: str
    longitude: float
    latitude: float
    points: int
    difficulty: str
    @staticmethod
    def calculate_difficulty(points):
        """Calculates difficulty based on points."""
        if points is None:
            return "UNKNOWN"

        if points <= 250:
            return "EASY"
        elif points <= 750:
            return "MEDIUM"
        else:
            return "HARD"


class PollutionSimple(PollutionBase):
    model_config = ConfigDict(from_attributes=True,)
    id: int
    stage: str = StagePollutionEnum.DETECTED
    owner_id: int



class PollutionPublic(PollutionSimple):
    performers: List["UserSimple"] = []
    images: Optional[List[FilePublic]] = []  # Список файлов

class PollutionCreate(PollutionBase):
    points: int

class PollutionUpdate(PollutionBase):
    model_config = ConfigDict(from_attributes=True)
    stage: str


from app.schemas.user import UserSimple
PollutionBase.update_forward_refs()


