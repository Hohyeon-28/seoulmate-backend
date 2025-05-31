from fastapi import FastAPI
from app.api import place
from app.api import event
from app.api import interest
from app.api import auth


app = FastAPI()
app.include_router(place.router, prefix="/api")
app.include_router(event.router, prefix="/api") 
app.include_router(interest.router)
app.include_router(auth.router)