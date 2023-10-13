from datetime import datetime
from typing import Optional

from sqlalchemy import select, or_
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
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            session: AsyncSession
    ) -> list[Reservation]:
        """Свободен ли запрошенный интервал времени"""
        # если это время полностью или частично зарезервировано в
        # каких-то объектах бронирования — метод возвращает
        # список этих объектов.
        # reservations = await session.execute(
        #     select(Reservation).filter(
        #         or_(Reservation.to_reserve < from_reserve,
        #             Reservation.from_reserve > to_reserve)
        #     )
        # )
        # reservations = reservations.scalars().all()
        # return reservations
        return []


reservation_crud = CRUDReservation(Reservation)
