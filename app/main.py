from fastapi import FastAPI
from app.api import place
from app.api import event
from app.api import interest
from app.api import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(place.router, prefix="/api")
app.include_router(event.router, prefix="/api") 
app.include_router(interest.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)