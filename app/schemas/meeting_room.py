from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomDB(MeetingRoomBase):
    id: int

    class Config:
        # Укажет модели Pydantic прочитать данные, даже если это не dictмодель,
        # а ORM (или любой другой произвольный объект с атрибутами)
        orm_mode = True


class MeetingRoomUpdate(MeetingRoomBase):

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя не может быть null')
        return value