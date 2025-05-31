from pydantic import BaseModel
from typing import Optional, Dict, Any, Union

class EventCreate(BaseModel):
    place_id: int
    title: str
    start_date: str
    end_date: Optional[str]
    target: Optional[str]
    price: Optional[str]
    is_free: Optional[str]
    image_url: Optional[str]
    detail_url: Optional[str]



class EventOut(BaseModel):
    event_id: int
    title: str
    start_date: str
    end_date: Optional[str]
    target: Optional[str]
    price: Optional[str]
    is_free: Optional[str]
    image_url: Optional[str]
    detail_url: Optional[str]
    category: Optional[str]    
    expected_attendees: Optional[Union[int, str]] 
    expected_attendance_by_hour: Optional[Dict[str, int]]
    
    #  place 관련 정보도 포함되어야 함
    place_id: int
    place_name: Optional[str]
    latitude: float
    longitude: float
    
    class Config:
        orm_mode = True
