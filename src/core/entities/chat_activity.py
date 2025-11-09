"""
ChatActivity entity - Domain model for chat activity
"""
import random
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .score_config import ScoreConfig


@dataclass
class ChatActivity:
    """채팅 활동 도메인 엔티티"""

    id: int
    user_id: int
    message_id: int
    base_score: int
    is_jackpot: bool
    multiplier: int
    final_score: int
    created_at: datetime

    @staticmethod
    def create_activity(
        user_id: int,
        message_id: int,
        config: "ScoreConfig",
    ) -> "ChatActivity":
        """채팅 활동 생성 (점수 계산 포함)

        Args:
            user_id: 사용자 ID
            message_id: 메시지 ID
            config: 점수 설정

        Returns:
            ChatActivity: 생성된 채팅 활동 엔티티
        """
        # 기본 점수 생성
        base_score = random.randint(config.chat_score_min, config.chat_score_max)

        # 잭팟 확률 체크
        is_jackpot = random.random() < config.jackpot_chance

        # 잭팟이면 배율 적용
        if is_jackpot:
            multiplier = random.randint(config.multiplier_min, config.multiplier_max)
            final_score = base_score * multiplier
        else:
            multiplier = 1
            final_score = base_score

        return ChatActivity(
            id=0,  # DB에서 할당됨
            user_id=user_id,
            message_id=message_id,
            base_score=base_score,
            is_jackpot=is_jackpot,
            multiplier=multiplier,
            final_score=final_score,
            created_at=datetime.now(),
        )

    def __str__(self) -> str:
        if self.is_jackpot:
            return (
                f"ChatActivity(jackpot! {self.base_score} x {self.multiplier} "
                f"= {self.final_score})"
            )
        return f"ChatActivity(score={self.final_score})"
