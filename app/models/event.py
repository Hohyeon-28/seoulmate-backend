# app/models/event.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Event(Base):
    __tablename__ = "event"

    event_id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("place.place_id"), nullable=False)
    title = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=True)
    target = Column(String, nullable=True)
    price = Column(String, nullable=True)
    is_free = Column(String, nullable=True)  # 유료 / 무료
    image_url = Column(String, nullable=True)
    detail_url = Column(String, nullable=True)

    category = Column(String, nullable=False)   # 공연, 전시 등
    expected_attendees = Column(Integer, nullable=True)  # 예상 참여 인원수
    expected_attendance_by_hour = Column(JSON, nullable=True)  # 새로 추가
  
    place = relationship("Place", back_populates="events")
    interests = relationship("Interest", back_populates="event")

    __table_args__ = (
        UniqueConstraint("place_id", "title", name="event_unique_place_title"),
    )
