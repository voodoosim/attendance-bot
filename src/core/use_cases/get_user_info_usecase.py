"""
GetUserInfo Use Case - 사용자 정보 조회 로직
"""
from dataclasses import dataclass
from typing import List

from src.core.entities.attendance import Attendance
from src.core.entities.chat_activity import ChatActivity
from src.core.entities.user import User
from src.core.exceptions import UserNotRegisteredError
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.chat_activity_repository import ChatActivityRepository
from src.repositories.user_repository import UserRepository


@dataclass
class UserInfoResult:
    """사용자 정보 결과"""

    user: User
    recent_attendances: List[Attendance]
    top_jackpots: List[ChatActivity]


class GetUserInfoUseCase:
    """사용자 정보 조회 유스케이스"""

    def __init__(
        self,
        user_repo: UserRepository,
        attendance_repo: AttendanceRepository,
        chat_activity_repo: ChatActivityRepository,
    ):
        self.user_repo = user_repo
        self.attendance_repo = attendance_repo
        self.chat_activity_repo = chat_activity_repo

    async def execute(self, telegram_id: int) -> UserInfoResult:
        """사용자 정보 조회

        Args:
            telegram_id: 텔레그램 사용자 ID

        Returns:
            UserInfoResult: 사용자 정보

        Raises:
            UserNotRegisteredError: 등록되지 않은 사용자
        """
        # 1. 사용자 조회
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotRegisteredError("먼저 .출첵 명령어로 등록해주세요!")

        # 2. 최근 출석 기록 조회 (최근 7일)
        recent_attendances = await self.attendance_repo.get_by_user(user.id, limit=7)

        # 3. 최고 잭팟 기록 조회 (상위 5개)
        top_jackpots = await self.chat_activity_repo.get_jackpots_by_user(
            user.id, limit=5
        )

        return UserInfoResult(
            user=user, recent_attendances=recent_attendances, top_jackpots=top_jackpots
        )
