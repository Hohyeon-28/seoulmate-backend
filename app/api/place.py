from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.place import insert_place
from app.schemas.place import PlaceCreate
import csv

router = APIRouter()

# 안전하게 dong_info 불러오기
dong_info = []
try:
    with open("dong_info.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if not row["위도"] or not row["경도"] or not row["인구수"]:
                    continue
                dong_info.append({
                    "district": row["시군구"].strip(),
                    "dong": row["읍면동/구"].strip() or row["읍/면/리/동"].strip(),
                    "latitude": float(row["위도"]),
                    "longitude": float(row["경도"]),
                    "population": int(float(row["인구수"]))
                })
            except (ValueError, KeyError) as e:
                continue
except FileNotFoundError:
    print("[ERROR] dong_info.csv 파일을 찾을 수 없습니다.")

# API 엔드포인트
@router.post("/places/")
def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    return insert_place(db, place.dict(), dong_info)
