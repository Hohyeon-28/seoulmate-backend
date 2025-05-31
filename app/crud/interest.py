# app/crud/interest.py

from sqlalchemy.orm import Session
from app.models.interest import Interest
from app.schemas.interest import InterestCreate
from datetime import datetime
from typing import List

def create_interest(db: Session, interest_data: InterestCreate) -> Interest:
    existing = db.query(Interest).filter_by(
        user_id=interest_data.user_id,
        event_id=interest_data.event_id
    ).first()
    if existing:
        return existing

    # 문자열을 datetime으로 파싱
    parsed_time = datetime.strptime(interest_data.bookmarked_at, "%Y-%m-%dT%H:%M")

    new_interest = Interest(
        user_id=interest_data.user_id,
        event_id=interest_data.event_id,
        bookmarked_at=parsed_time.replace(second=0, microsecond=0)
    )
    db.add(new_interest)
    db.commit()
    db.refresh(new_interest)
    return new_interest



def get_interests_by_user(db: Session, user_id: int) -> List[Interest]:
    return db.query(Interest).filter_by(user_id=user_id).all()