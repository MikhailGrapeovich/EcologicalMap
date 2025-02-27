from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    text: str