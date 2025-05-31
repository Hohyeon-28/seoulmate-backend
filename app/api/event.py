# app/api/event.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.event import create_event, get_events_by_place, get_event
from app.schemas.event import EventCreate, EventOut
from typing import List, Optional
from app.crud.event import search_events
from fastapi import Query
from datetime import date

router = APIRouter()

@router.post("/events/", response_model=EventOut)
def create_event_api(event: EventCreate, db: Session = Depends(get_db)):
    return create_event(db, event)


@router.get("/events/search", response_model=List[EventOut])
def search_events_api(
    district: Optional[str] = Query(None),
    dong: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    target_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    return search_events(db, district, dong, category)


@router.get("/events/{event_id}", response_model=EventOut)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get("/places/{place_id}/events", response_model=List[EventOut])
def read_events_by_place(place_id: int, db: Session = Depends(get_db)):
    return get_events_by_place(db, place_id)
