"""
User entity - Domain model for user
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """사용자 도메인 엔티티"""

    id: int
    telegram_id: int
    username: str
    total_score: int
    chat_count: int
    jackpot_count: int
    max_jackpot: int
    consecutive_days: int
    total_attendance: int
    last_checkin: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    def can_checkin_today(self) -> bool:
        """오늘 출석 가능 여부 확인

        Returns:
            bool: 출석 가능하면 True, 이미 했으면 False
        """
        if not self.last_checkin:
            return True

        today = datetime.now().date()
        last_checkin_date = self.last_checkin.date()

        return last_checkin_date < today

    def calculate_consecutive_days(self) -> int:
        """연속 출석일 계산

        Returns:
            int: 계산된 연속 출석일
        """
        if not self.last_checkin:
            return 1

        today = datetime.now().date()
        last_checkin_date = self.last_checkin.date()
        days_diff = (today - last_checkin_date).days

        # 어제 출석했으면 연속 유지
        if days_diff == 1:
            return self.consecutive_days + 1

        # 그 외에는 연속 끊김
        return 1

    def add_score(self, score: int) -> None:
        """점수 추가

        Args:
            score: 추가할 점수
        """
        self.total_score += score
        self.updated_at = datetime.now()

    def increment_chat_count(self) -> None:
        """채팅 수 증가"""
        self.chat_count += 1
        self.updated_at = datetime.now()

    def record_jackpot(self, jackpot_score: int) -> None:
        """잭팟 기록

        Args:
            jackpot_score: 잭팟 점수
        """
        self.jackpot_count += 1
        if jackpot_score > self.max_jackpot:
            self.max_jackpot = jackpot_score
        self.updated_at = datetime.now()

    def update_checkin(self, consecutive_days: int) -> None:
        """출석 정보 업데이트

        Args:
            consecutive_days: 연속 출석일
        """
        self.consecutive_days = consecutive_days
        self.total_attendance += 1
        self.last_checkin = datetime.now()
        self.updated_at = datetime.now()

    @property
    def average_score_per_chat(self) -> float:
        """채팅당 평균 점수

        Returns:
            float: 평균 점수 (채팅 수가 0이면 0.0)
        """
        if self.chat_count == 0:
            return 0.0
        return round(self.total_score / self.chat_count, 2)
