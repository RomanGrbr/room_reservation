from typing import Optional

from sqlalchemy import select
# Класс асинхронной сессии для аннотаций.
from sqlalchemy.ext.asyncio import AsyncSession
# Конвертирует в JSON-формат как объекты из базы данных, так и Pydantic-модели
from fastapi.encoders import jsonable_encoder

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession
) -> MeetingRoom:
    # Конвертируем объект MeetingRoomCreate в словарь.
    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)
    # Добавляем созданный объект в сессию.
    session.add(db_room)
    # Записываем изменения непосредственно в БД.
    await session.commit()
    # Обновляем объект, считываем данные из БД, чтобы получить его id.
    await session.refresh(db_room)
    return db_room


async def get_room_id_by_name(
        room_name: str,
        session: AsyncSession
) -> Optional[int]:
    """Получить комнату по имени"""
    # Получаем объект класса Result.
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    # Извлекаем из него конкретное значение.
    return db_room_id.scalars().first()


async def read_all_rooms_from_db(
        session: AsyncSession) -> list[MeetingRoom]:
    """Получить все комнаты из базы"""
    rooms = await session.execute(select(MeetingRoom))
    return rooms.scalars().all()


async def get_meeting_room_by_id(
        room_id: int, session: AsyncSession
) -> Optional[MeetingRoom]:
    """Получить комнату по id"""
    db_room = await session.get(MeetingRoom, room_id)
    return db_room


async def update_meeting_room(
        db_room: MeetingRoom,
        room_in: MeetingRoomUpdate,
        session: AsyncSession
) -> MeetingRoom:
    """Обновить комнату"""
    # конвертировать в JSON-формат
    obj_data = jsonable_encoder(db_room)
    # Перевести в словарь и исключить поля,
    # которые не были установлены пользователем.
    update_data = room_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_room, field, update_data[field])
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room
