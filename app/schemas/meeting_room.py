from typing import Optional

from pydantic import BaseModel, Field


class MeetingRoomCreate(BaseModel):
    name: str = Field(..., max_length=100,
                      title='Название переговорной комнаты')
    description: Optional[str]
