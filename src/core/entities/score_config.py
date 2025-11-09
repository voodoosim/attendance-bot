"""
ScoreConfig entity - Domain model for score configuration
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ScoreConfig:
    """점수 설정 도메인 엔티티"""

    id: int
    attendance_score: int
    chat_score_min: int
    chat_score_max: int
    jackpot_chance: float
    multiplier_min: int
    multiplier_max: int
    max_consecutive_bonus: int
    updated_at: Optional[datetime]

    @staticmethod
    def default() -> "ScoreConfig":
        """기본 점수 설정 반환

        Returns:
            ScoreConfig: 기본 설정값
        """
        return ScoreConfig(
            id=1,
            attendance_score=10,
            chat_score_min=1,
            chat_score_max=6,
            jackpot_chance=0.05,  # 5%
            multiplier_min=1,
            multiplier_max=7,
            max_consecutive_bonus=7,
            updated_at=datetime.now(),
        )

    def validate(self) -> bool:
        """설정값 유효성 검사

        Returns:
            bool: 유효하면 True
        """
        if self.attendance_score < 0:
            return False
        if self.chat_score_min < 0 or self.chat_score_max < self.chat_score_min:
            return False
        if not 0 <= self.jackpot_chance <= 1:
            return False
        if self.multiplier_min < 1 or self.multiplier_max < self.multiplier_min:
            return False
        if self.max_consecutive_bonus < 0:
            return False
        return True

    def __str__(self) -> str:
        return (
            f"ScoreConfig(attendance={self.attendance_score}, "
            f"chat={self.chat_score_min}-{self.chat_score_max}, "
            f"jackpot={self.jackpot_chance*100}%)"
        )
