# utils/predict.py
import random

def predict_attendees(category: str, population: int) -> int:
    """카테고리와 인구수를 기반으로 예상 참여 인원 예측"""
    base_ratio = {
        "전시/미술": 0.015,
        "공연예술": 0.03,
        "축제/행사": 0.05,
        "교육/체험": 0.025,
        "기타": 0.02
    }
    ratio = base_ratio.get(category, 0.02)
    noise = random.uniform(0.9, 1.1)  # ±10% 노이즈
    return int(population * ratio * noise)

def predict_attendance_by_hour(population: int, category: str) -> dict:
    """시간대별 참석 인원 예측 함수 (랜덤한 분포 적용, 패턴 저장 없이)"""
    base = population * 0.01

    if category == "공연예술":
        raw_factors = {
            "10:00": random.uniform(0.01, 0.07),
            "11:00": random.uniform(0.02, 0.1),
            "12:00": random.uniform(0.05, 0.15),
            "13:00": random.uniform(0.1, 0.2),
            "14:00": random.uniform(0.1, 0.25),
            "15:00": random.uniform(0.1, 0.25),
            "16:00": random.uniform(0.1, 0.3),
            "17:00": random.uniform(0.1, 0.3),
            "18:00": random.uniform(0.1, 0.3),
        }
    elif category == "전시/미술":
        raw_factors = {
            "10:00": random.uniform(0.1, 0.2),
            "11:00": random.uniform(0.1, 0.25),
            "12:00": random.uniform(0.1, 0.25),
            "13:00": random.uniform(0.1, 0.15),
            "14:00": random.uniform(0.1, 0.1),
            "15:00": random.uniform(0.1, 0.05),
            "16:00": random.uniform(0.05, 0.3),
            "17:00": random.uniform(0.05, 0.2),
            "18:00": random.uniform(0.01, 0.35),
        }
    elif category == "축제/행사":
        raw_factors = {
            "10:00": random.uniform(0.05, 0.1),
            "11:00": random.uniform(0.05, 0.1),
            "12:00": random.uniform(0.1, 0.2),
            "13:00": random.uniform(0.1, 0.2),
            "14:00": random.uniform(0.1, 0.2),
            "15:00": random.uniform(0.1, 0.2),
            "16:00": random.uniform(0.1, 0.2),
            "17:00": random.uniform(0.1, 0.2),
            "18:00": random.uniform(0.1, 0.2),
        }
    elif category == "교육/체험":
        raw_factors = {
            "10:00": random.uniform(0.1, 0.25),
            "11:00": random.uniform(0.1, 0.25),
            "12:00": random.uniform(0.1, 0.2),
            "13:00": random.uniform(0.1, 0.15),
            "14:00": random.uniform(0.1, 0.2),
            "15:00": random.uniform(0.05, 0.15),
            "16:00": random.uniform(0.05, 0.1),
            "17:00": random.uniform(0.05, 0.15),
            "18:00": random.uniform(0.01, 0.1),
        }
    else:  # 기타
        raw_factors = {
            hour: random.uniform(0.08, 0.12)
            for hour in [
                "10:00", "11:00", "12:00", "13:00",
                "14:00", "15:00", "16:00", "17:00", "18:00"
            ]
        }

    # 정규화 (합이 1이 되도록)
    total = sum(raw_factors.values())
    normalized = {hour: round(val / total, 4) for hour, val in raw_factors.items()}
    return {hour: int(base * ratio) for hour, ratio in normalized.items()}
