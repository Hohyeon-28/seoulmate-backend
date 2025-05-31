# app/api/interest.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.interest import InterestCreate, InterestOut
from app.crud.interest import create_interest
from app.models.interest import Interest
from datetime import datetime
from app.crud.interest import get_interests_by_user
from typing import List

router = APIRouter(prefix="/api/interests")

def format_interest(interest: Interest) -> dict:
    return {
        "interest_id": interest.interest_id,
        "user_id": interest.user_id,
        "event_id": interest.event_id,
        "bookmarked_at": interest.bookmarked_at.strftime("%Y-%m-%dT%H:%M")
    }

@router.post("/", response_model=InterestOut)
def add_interest(interest: InterestCreate, db: Session = Depends(get_db)):
    new_interest = create_interest(db, interest)
    return format_interest(new_interest)  # 포맷팅된 dict 리턴


@router.get("/user/{user_id}", response_model=List[InterestOut])
def get_user_interests(user_id: int, db: Session = Depends(get_db)):
    interests = get_interests_by_user(db, user_id)
    # bookmarked_at 포맷 정리
    return [
        {
            "interest_id": i.interest_id,
            "user_id": i.user_id,
            "event_id": i.event_id,
            "bookmarked_at": i.bookmarked_at.strftime("%Y-%m-%dT%H:%M")
        } for i in interests
    ]