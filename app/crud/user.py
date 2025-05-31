from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import SignupRequest
from fastapi import HTTPException

def authenticate_user(db: Session, user_id: int, hashed_password: str) -> User | None:
    user = db.query(User).filter_by(user_id=user_id).first()
    if user and user.hashed_password == hashed_password:
        return user
    return None



def create_user(db: Session, signup_data: SignupRequest) -> User:
    # 중복 검사
    existing = db.query(User).filter(
        (User.user_id == signup_data.user_id) | 
        (User.email == signup_data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User ID or email already exists")

    new_user = User(
        user_id=signup_data.user_id,
        email=signup_data.email,
        hashed_password=signup_data.hashed_password,
        age=signup_data.age,
        preferred_genre=signup_data.preferred_genre
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user