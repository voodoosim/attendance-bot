"""
ProcessMessage Use Case - 메시지 처리 및 점수 부여 로직
"""
from dataclasses import dataclass
from typing import Optional

from src.core.entities.chat_activity import ChatActivity
from src.core.entities.user import User
from src.core.exceptions import UserNotRegisteredError
from src.repositories.chat_activity_repository import ChatActivityRepository
from src.repositories.score_config_repository import ScoreConfigRepository
from src.repositories.user_repository import UserRepository


@dataclass
class ProcessMessageResult:
    """메시지 처리 결과"""

    user: User
    activity: ChatActivity
    is_jackpot: bool


class ProcessMessageUseCase:
    """메시지 처리 유스케이스"""

    def __init__(
        self,
        user_repo: UserRepository,
        chat_activity_repo: ChatActivityRepository,
        config_repo: ScoreConfigRepository,
    ):
        self.user_repo = user_repo
        self.chat_activity_repo = chat_activity_repo
        self.config_repo = config_repo

    async def execute(
        self, telegram_id: int, message_id: int
    ) -> Optional[ProcessMessageResult]:
        """메시지 처리 및 점수 부여

        Args:
            telegram_id: 텔레그램 사용자 ID
            message_id: 메시지 ID

        Returns:
            ProcessMessageResult: 메시지 처리 결과 (미등록 유저는 None)
        """
        # 1. 등록된 사용자인지 확인
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            # 미등록 유저는 무시 (None 반환)
            return None

        # 2. 점수 설정 조회
        config = await self.config_repo.get_config()

        # 3. 채팅 활동 생성 (점수 계산 포함)
        activity = ChatActivity.create_activity(
            user_id=user.id, message_id=message_id, config=config
        )

        # 4. 채팅 활동 저장
        await self.chat_activity_repo.create(activity)

        # 5. 사용자 정보 업데이트
        user.add_score(activity.final_score)
        user.increment_chat_count()

        if activity.is_jackpot:
            user.record_jackpot(activity.final_score)

        await self.user_repo.update(user)

        return ProcessMessageResult(
            user=user, activity=activity, is_jackpot=activity.is_jackpot
        )
