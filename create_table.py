# create_tables.py
from app.database import Base, engine
from app.models.place import Place  
from app.models.event import Event
from app.models.user import User
from app.models.interest import Interest

# 실제 DB에 테이블 생성
Base.metadata.create_all(bind=engine)
print("테이블 생성 완료")
