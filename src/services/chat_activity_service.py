"""
ChatActivity Service - 채팅 활동 관련 비즈니스 서비스
"""
from typing import Optional, Dict, Any

from src.core.use_cases.process_message_usecase import ProcessMessageUseCase


class ChatActivityService:
    """채팅 활동 서비스"""

    def __init__(self, process_message_usecase: ProcessMessageUseCase):
        self.process_message_usecase = process_message_usecase

    async def process_message(
        self, telegram_id: int, message_id: int
    ) -> Optional[Dict[str, Any]]:
        """메시지 처리 및 점수 부여

        Args:
            telegram_id: 텔레그램 사용자 ID
            message_id: 메시지 ID

        Returns:
            Dict: 처리 결과 (미등록 유저는 None)
        """
        result = await self.process_message_usecase.execute(telegram_id, message_id)

        if not result:
            return None  # 미등록 유저

        return {
            "user": result.user,
            "activity": result.activity,
            "is_jackpot": result.is_jackpot,
        }
