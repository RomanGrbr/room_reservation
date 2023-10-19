from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, root_validator, validator


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)
    user_id: Optional[int]

    class Config:
        # Запретить пользователю передавать параметры, не описанные в схеме
        extra = Extra.forbid


class ReservationUpdate(ReservationBase):
    """Обновить запись"""

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value: str):
        """Валидатор поля from_reserve"""
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    # Корневой валидатор не должен вызываться, если при валидации
    # отдельных полей вернётся ошибка - skip_on_failure=True
    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        """Валидатор по полям from_reserve и to_reserve"""
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return values


class ReservationCreate(ReservationUpdate):
    """Создать запись"""
    meetingroom_id: int


class ReservationDB(ReservationBase):
    """Получить запись из базы"""
    id: int
    meetingroom_id: int

    class Config:
        # Укажет модели Pydantic прочитать данные, даже если это не dictмодель,
        # а ORM (или любой другой произвольный объект с атрибутами)
        orm_mode = True
