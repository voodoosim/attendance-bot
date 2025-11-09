"""
Attendance Service - 출석 관련 비즈니스 서비스
"""
from typing import Dict, Any

from src.core.exceptions import AlreadyCheckedInError
from src.core.use_cases.check_in_usecase import CheckInUseCase


class AttendanceService:
    """출석 관련 서비스"""

    def __init__(self, checkin_usecase: CheckInUseCase):
        self.checkin_usecase = checkin_usecase

    async def check_in(self, telegram_id: int, username: str) -> Dict[str, Any]:
        """출석 체크 처리

        Args:
            telegram_id: 텔레그램 사용자 ID
            username: 사용자 이름

        Returns:
            Dict: 출석 결과
        """
        try:
            result = await self.checkin_usecase.execute(telegram_id, username)
            return {
                "success": True,
                "user": result.user,
                "score": result.score,
                "consecutive_days": result.consecutive_days,
                "is_new_user": result.is_new_user,
            }
        except AlreadyCheckedInError as e:
            return {"success": False, "error": str(e)}
