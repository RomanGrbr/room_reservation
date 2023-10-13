from fastapi import APIRouter, Depends

# Класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
# from app.crud.meeting_room import (
#     create_meeting_room, get_room_id_by_name,
#     read_all_rooms_from_db, update_meeting_room,
#     get_meeting_room_by_id, delete_meeting_room
# )
# Вместо импортов 6 функций
from app.crud.meeting_room import meeting_room_crud
from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
)
# from app.models.meeting_room import MeetingRoom
from app.api.validators import check_name_duplicate, check_meeting_room_exists

# router = APIRouter(
#     prefix='/meeting_rooms',
#     tags=['Meeting Rooms']  # Объединить одним тегом
#     )
router = APIRouter()


@router.get(
        '/',
        response_model=list[MeetingRoomDB],
        response_model_exclude_none=True,
    )
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session),
):
    # all_rooms = await read_all_rooms_from_db(session)
    # Заменил вызов функции на вызов метода.
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.post(
        '/',
        response_model=MeetingRoomDB,  # Указываем схему ответа.
        response_model_exclude_none=True,  # Исключить поля с None из ответа.
        # response_model_exclude_unset Исключать поля, которые не были установлены
        # response_model_exclude_defaults Исключать значения по умолчанию
    )
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(meeting_room.name, session)
    # new_room = await create_meeting_room(meeting_room, session)
    # Заменил вызов функции на вызов метода.
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.patch(
        '/{meeting_room_id}',
        response_model=MeetingRoomDB,
        response_model_exclude_none=True,
)
async def partially_update_meeting_room(
    meeting_room_id: int,
    obj_in: MeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)
    # meeting_room = await update_meeting_room(
    #     meeting_room, obj_in, session
    # )
    # Заменил вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    # meeting_room = await delete_meeting_room(
    #     meeting_room, session
    # )
    # Заменил вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room
