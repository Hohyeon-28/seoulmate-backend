from pydantic import BaseModel

class PlaceCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    category: str
