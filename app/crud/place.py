from app.models.place import Place
from sqlalchemy.orm import Session
from app.utils.location import find_nearest_dong
from app.utils.predict import predict_attendees

def insert_place(db: Session, place_data: dict, dong_info: list):
    # 1. KNN 또는 거리 기반으로 가장 가까운 동 찾기
    matched_dong = find_nearest_dong(place_data["latitude"], place_data["longitude"], dong_info)

    # 2. 인구 정보 추출
    population = matched_dong["population"]
    district = matched_dong["district"]
    dong = matched_dong["dong"]

    # 3. 예상 참여 인원 계산
    expected = predict_attendees(category=place_data["category"], population=population)

    # 4. DB 저장
    new_place = Place(
        name=place_data["name"],
        latitude=place_data["latitude"],
        longitude=place_data["longitude"],
        category=place_data["category"],
        district=district,
        dong=dong,
        population=population,
        expected_attendees=expected
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place
