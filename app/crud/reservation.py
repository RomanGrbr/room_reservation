from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

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
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            session: AsyncSession
    ) -> list[Reservation]:
        """Свободен ли запрошенный интервал времени"""
        # если это время полностью или частично зарезервировано в
        # каких-то объектах бронирования — метод возвращает
        # список этих объектов.
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                and_(
                    from_reserve <= Reservation.to_reserve,
                    to_reserve >= Reservation.from_reserve
                )
            )
        )
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
