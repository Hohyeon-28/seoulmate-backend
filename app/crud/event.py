# app/crud/event.py

from sqlalchemy.orm import Session, joinedload
from app.models.event import Event
from app.models.place import Place
from app.schemas.event import EventCreate
from sqlalchemy import cast, Date
from datetime import datetime, date
from typing import Optional

def create_event(db: Session, event_data: EventCreate) -> Event:
    new_event = Event(**event_data.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def get_events_by_place(db: Session, place_id: int):
    return db.query(Event).filter(Event.place_id == place_id).all()

def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.event_id == event_id).first()

def search_events(
    db: Session,
    district: Optional[str] = None,
    dong: Optional[str] = None,
    category: Optional[str] = None,
    target_date: Optional[date] = None
):
    # 오늘 날짜, 현재 시간
    now = datetime.now()
    today = now.date()
    now_hour_int = now.hour  # 예: 14 (int)

    # target_date가 없으면 기본은 오늘
    if not target_date:
        target_date = today

    # 기본 쿼리: target_date가 start_date ~ end_date 범위에 포함되는 이벤트만
    query = (
        db.query(Event)
        .options(joinedload(Event.place))
        .join(Place)
        .filter(
            cast(Event.start_date, Date) <= target_date,
            cast(Event.end_date, Date) >= target_date
        )
    )

    # 필터: 지역명, 동명, 카테고리
    if district:
        query = query.filter(Place.district == district)
    if dong:
        query = query.filter(Place.dong == dong)
    if category:
        query = query.filter(Event.category != None)
        query = query.filter(Event.category.ilike(f"%{category}%"))

    events = query.all()
    result = []

    for e in events:
        hourly = e.expected_attendance_by_hour or {}

        # 현재 예상 인원
        current_hour_str = now.strftime("%H:00")
        expected_now = hourly.get(current_hour_str)


        result.append({
            "event_id": e.event_id,
            "title": e.title,
            "start_date": str(e.start_date),
            "end_date": str(e.end_date),
            "target": e.target,
            "price": e.price,
            "is_free": e.is_free,
            "image_url": e.image_url,
            "detail_url": e.detail_url,
            "place_id": e.place_id,
            "place_name": e.place.name,
            "category": e.category,
            "expected_attendees": expected_now if expected_now is not None else "현재 운영 중이 아님",
            "expected_attendance_by_hour": hourly
        })

    return result

def get_events_by_date(db: Session, target_date: date, district: Optional[str] = None):
    query = db.query(Event).join(Place).filter(
        cast(Event.start_date, Date) <= target_date,
        cast(Event.end_date, Date) >= target_date
    )
    if district:
        query = query.filter(Place.district == district)
    return query.all()
