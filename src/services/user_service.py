"""
User Service - 사용자 정보 관련 비즈니스 서비스
"""
from typing import Dict, Any

from src.core.exceptions import UserNotRegisteredError
from src.core.use_cases.get_ranking_usecase import GetRankingUseCase, RankingType
from src.core.use_cases.get_user_info_usecase import GetUserInfoUseCase


class UserService:
    """사용자 서비스"""

    def __init__(
        self,
        get_user_info_usecase: GetUserInfoUseCase,
        get_ranking_usecase: GetRankingUseCase,
    ):
        self.get_user_info_usecase = get_user_info_usecase
        self.get_ranking_usecase = get_ranking_usecase

    async def get_user_info(self, telegram_id: int) -> Dict[str, Any]:
        """사용자 정보 조회

        Args:
            telegram_id: 텔레그램 사용자 ID

        Returns:
            Dict: 사용자 정보
        """
        try:
            result = await self.get_user_info_usecase.execute(telegram_id)
            return {
                "success": True,
                "user": result.user,
                "recent_attendances": result.recent_attendances,
                "top_jackpots": result.top_jackpots,
            }
        except UserNotRegisteredError as e:
            return {"success": False, "error": str(e)}

    async def get_ranking(
        self, ranking_type: RankingType, limit: int = 10
    ) -> Dict[str, Any]:
        """랭킹 조회

        Args:
            ranking_type: 랭킹 타입
            limit: 조회할 사용자 수

        Returns:
            Dict: 랭킹 정보
        """
        result = await self.get_ranking_usecase.execute(ranking_type, limit)
        return {
            "success": True,
            "ranking_type": result.ranking_type,
            "users": result.users,
        }
