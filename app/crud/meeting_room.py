from typing import Optional

from sqlalchemy import select
# Класс асинхронной сессии для аннотаций.
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


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
    # Получаем объект класса Result.
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    # Извлекаем из него конкретное значение.
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def read_all_rooms_from_db(
        session: AsyncSession) -> list[MeetingRoom]:
    rooms = await session.execute(select(MeetingRoom))
    return rooms.scalars().all()
