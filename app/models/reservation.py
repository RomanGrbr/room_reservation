from sqlalchemy import Column, DateTime, Integer, ForeignKey

from app.core.db import Base


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetengroom_id = Column(Integer, ForeignKey('meetingroom.id'))
