from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(
    CRUDBase[
        Reservation,
        ReservationCreate,
        ReservationUpdate
    ]
):
    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
            **kwargs
    ) -> list[Reservation]:
        """Свободен ли запрошенный интервал времени"""
        # если это время полностью или частично зарезервировано в
        # каких-то объектах бронирования — метод возвращает
        # список этих объектов.
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        # Если передан id бронирования...
        if reservation_id is not None:
            # ... то к выражению нужно добавить новое условие.
            select_stmt = select_stmt.where(
                # id искомых объектов не равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession
    ):
        reservations = await session.execute(select(Reservation).where(
            Reservation.id == room_id,
            Reservation.to_reserve > datetime.now()
        ))
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
