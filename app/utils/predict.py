def predict_attendees(category: str, population: int) -> int:
    # 기본 참여율 설정
    base_ratio = {
        "공연": 0.03,
        "전시": 0.015,
        "축제": 0.05,
        "기타": 0.02
    }
    ratio = base_ratio.get(category, 0.02)

    # 노이즈 추가 (±10%)
    import random
    noise = random.uniform(0.9, 1.1)

    return int(population * ratio * noise)


def predict_attendance_by_hour(population, category):
    """시간대별 참석 인원 예측 함수"""
    base = population * 0.01  # 예시: 전체의 1%가 행사 참여
    hourly_factors = {
        "10:00": 0.05,
        "11:00": 0.1,
        "12:00": 0.15,
        "13:00": 0.1,
        "14:00": 0.1,
        "15:00": 0.1,
        "16:00": 0.15,
        "17:00": 0.1,
        "18:00": 0.15
    }
    return {hour: int(base * factor) for hour, factor in hourly_factors.items()}
