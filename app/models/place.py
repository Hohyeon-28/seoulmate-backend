from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Place(Base):
    __tablename__ = "place"

    place_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    district = Column(String, nullable=False)  # 구
    dong = Column(String, nullable=False)      # 동
    population = Column(Integer, nullable=True)  # 해당 동 인구

    events = relationship("Event", back_populates="place")