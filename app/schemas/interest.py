from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InterestCreate(BaseModel):
    user_id: int
    event_id: int
    bookmarked_at: str 

class InterestOut(BaseModel):
    interest_id: int
    user_id: int
    event_id: int
    bookmarked_at: str

    class Config:
        orm_mode = True
