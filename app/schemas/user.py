# import datetime
# from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass
    # Если нужно расширить модель пользователя
    # first_name: str
    # birthdate: Optional[datetime.date]


class UserCreate(schemas.BaseUserCreate):
    pass
    # first_name: str
    # birthdate: Optional[datetime.date]


class UserUpdate(schemas.BaseUserUpdate):
    pass
    # first_name: Optional[str]
    # birthdate: Optional[datetime.date]
