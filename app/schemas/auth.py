from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_id: int
    hashed_password: str

class SignupRequest(BaseModel):
    user_id: int
    email: str
    hashed_password: str
    age: int
    preferred_genre: str