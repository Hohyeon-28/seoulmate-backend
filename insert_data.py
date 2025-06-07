# insert_data.py
# place.csv에서 Place와 Event 테이블에 동시에 insert하는 스크립트
from sqlalchemy.orm import Session
from app.models.place import Place
from app.models.event import Event
from app.models.user import User
from app.models.interest import Interest
from app.utils.location import find_nearest_dong
from app.utils.predict import predict_attendees, predict_attendance_by_hour
from app.database import SessionLocal
from datetime import timezone
import csv
import pandas as pd

# dong_info는 외부에서 불러오도록 전달받음 (예: dong_info.csv 파싱 후 dict list)
def insert_places_and_events_from_csv(db: Session, csv_path: str, dong_info: list):
    seen_events = set()  # (place_id, title) 조합 저장용

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 열 이름과 값 모두 공백 제거
            row = {k.strip(): v.strip() for k, v in row.items()}

            if not row["위도"] or not row["경도"]:
                print(f"[SKIP] 위도 또는 경도 누락됨: {row}")
                continue

            try:
                lat = float(row["위도"])
                lon = float(row["경도"])
            except ValueError:
                print(f"[SKIP] 위도/경도 변환 실패: {row['위도']}, {row['경도']}")
                continue

            place_name = row["장소"]

            # 동 매핑
            matched_dong = find_nearest_dong(lat, lon, dong_info)
            population = matched_dong["population"]
            district = matched_dong["district"]
            dong = matched_dong["dong"]

            # 장소 중복 확인
            place = db.query(Place).filter_by(name=place_name).first()
            if not place:
                place = Place(
                    name=place_name,
                    latitude=lat,
                    longitude=lon,
                    district=district,
                    dong=dong,
                    population=population,
                )
                db.add(place)
                db.commit()
                db.refresh(place)

            title = row["공연/행사명"]
            event_key = (place.place_id, title)

            # 이미 처리한 조합이면 스킵
            if event_key in seen_events:
                continue
            seen_events.add(event_key)

            # 기존 이벤트 중복 확인
            event = db.query(Event).filter_by(place_id=place.place_id, title=title).first()

            if event:
                event.start_date = row["시작일"]
                event.end_date = row["종료일"]
                event.target = row["이용대상"]
                event.price = row["이용요금"]
                event.is_free = row["유무료"]
                event.image_url = row["대표이미지"]
                event.detail_url = row["문화포털상세URL"]
                event.category = row["대분류"]
                event.expected_attendees = predict_attendees(row["대분류"], population)
                event.expected_attendance_by_hour = predict_attendance_by_hour(population, row["대분류"])
            else:
                event = Event(
                    place_id=place.place_id,
                    title=title,
                    start_date=row["시작일"],
                    end_date=row["종료일"],
                    target=row["이용대상"],
                    price=row["이용요금"],
                    is_free=row["유무료"],
                    image_url=row["대표이미지"],
                    detail_url=row["문화포털상세URL"],
                    category=row["대분류"],
                    expected_attendees=predict_attendees(row["대분류"], population),
                    expected_attendance_by_hour=predict_attendance_by_hour(population, row["대분류"])
                )
                db.add(event)

        db.commit()




def insert_users_and_interests_from_csv(db: Session, csv_path: str):
    df = pd.read_csv(csv_path)

    # 중복 없이 유저 데이터 추출
    users_df = df[["user_id", "email", "hashed_password", "age", "preferred_genre"]].drop_duplicates()

    # interest_id는 제거한 상태로 추출
    interests_df = df[["user_id", "event_id", "bookmarked_at"]].copy()
    interests_df["bookmarked_at"] = pd.to_datetime(interests_df["bookmarked_at"])
    interests_df["bookmarked_at"] = interests_df["bookmarked_at"].apply(
        lambda dt: dt.replace(second=0, microsecond=0)
    )

    # 유저 삽입
    for _, row in users_df.iterrows():
        user = db.query(User).filter_by(user_id=row.user_id).first()
        if not user:
            db_user = User(
                user_id=row.user_id,
                email=row.email,
                hashed_password=row.hashed_password,
                age=row.age,
                preferred_genre=row.preferred_genre
            )
            db.add(db_user)

    db.commit()

    # 관심 행사 삽입
    for _, row in interests_df.iterrows():
        interest = db.query(Interest).filter_by(user_id=row.user_id, event_id=row.event_id).first()
        if not interest:
            db_interest = Interest(
                user_id=row.user_id,
                event_id=row.event_id,
                bookmarked_at=row.bookmarked_at
            )
            db.add(db_interest)

    db.commit()




def load_dong_info(path: str):
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        dong_info = []
        for row in reader:
            if not row["위도"] or not row["경도"] or not row["인구수"]:
                continue
            try:
                dong_info.append({
                    "district": row["시군구"].strip(),
                    "dong": row["읍면동/구"].strip() or row["읍/면/리/동"].strip(),
                    "latitude": float(row["위도"]),
                    "longitude": float(row["경도"]),
                    "population": int(float(row["인구수"]))
                })
            except (ValueError, KeyError):
                continue
        return dong_info
    

if __name__ == "__main__":
    db = SessionLocal()
    dong_info = load_dong_info("dong_info.csv")
    insert_places_and_events_from_csv(
        db=db,
        csv_path="place.csv",
        dong_info=dong_info
    )
    insert_users_and_interests_from_csv(
        db=db,
        csv_path="user_interest.csv"
    )

    print("삽입 완료")