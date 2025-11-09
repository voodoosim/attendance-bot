"""
Attendance entity - Domain model for attendance record
"""
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Attendance:
    """출석 기록 도메인 엔티티"""

    id: int
    user_id: int
    date: date
    score: int
    consecutive_days: int
    created_at: datetime

    @staticmethod
    def calculate_score(base_score: int, consecutive_days: int, max_bonus: int) -> int:
        """출석 점수 계산

        Args:
            base_score: 기본 출석 점수
            consecutive_days: 연속 출석일
            max_bonus: 최대 보너스 점수

        Returns:
            int: 계산된 출석 점수
        """
        bonus = min(consecutive_days, max_bonus)
        return base_score + bonus

    def __str__(self) -> str:
        return f"Attendance(user_id={self.user_id}, date={self.date}, score={self.score})"
