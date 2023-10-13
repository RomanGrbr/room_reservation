from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models.meeting_room import MeetingRoom


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    # room_id = await get_room_id_by_name(room_name, session)
    # Заменил вызов функции на вызов метода.
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!')


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    """Проверяет наличие переговорки"""
    # meeting_room = await get_meeting_room_by_id(
    #     meeting_room_id, session
    # )
    # Заменил вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )


async def check_reservation_intersections(**kwargs) -> list[MeetingRoom]:
    """
    Eсли вызванный метод вернёт список броней —
    корутина-валидатор должна вернуть этот список в сообщении HTTPException
    """
    reservation = await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    if reservation:
        raise HTTPException(
            status_code=422,
            detail=str(reservation)
        )
