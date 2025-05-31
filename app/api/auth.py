from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import LoginRequest, SignupRequest
from app.crud.user import authenticate_user, create_user

router = APIRouter(prefix="/api/auth")

@router.post("/login")
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_req.user_id, login_req.hashed_password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user_id or password")
    return {"message": "Login successful", "user_id": user.user_id}

@router.post("/signup")
def signup(signup_req: SignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, signup_req)
    return {"message": "Signup successful", "user_id": user.user_id}