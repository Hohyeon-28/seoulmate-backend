# app/models/interest.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
from app.models.user import User
from app.models.event import Event

class Interest(Base):
    __tablename__ = "interests"

    interest_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    event_id = Column(Integer, ForeignKey("event.event_id"))
    bookmarked_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(second=0, microsecond=0)
    )
    user = relationship(User, back_populates="interests")
    event = relationship(Event, back_populates="interests")