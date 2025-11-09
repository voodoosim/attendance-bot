"""
GetRanking Use Case - 랭킹 조회 로직
"""
from dataclasses import dataclass
from enum import Enum
from typing import List

from src.core.entities.user import User
from src.repositories.user_repository import UserRepository


class RankingType(Enum):
    """랭킹 타입"""

    SCORE = "score"  # 점수 랭킹
    CHAT_COUNT = "chat_count"  # 채팅 수 랭킹
    JACKPOT = "jackpot"  # 잭팟 횟수 랭킹
    CONSECUTIVE_DAYS = "consecutive_days"  # 연속 출석 랭킹


@dataclass
class RankingResult:
    """랭킹 결과"""

    ranking_type: RankingType
    users: List[User]


class GetRankingUseCase:
    """랭킹 조회 유스케이스"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(
        self, ranking_type: RankingType, limit: int = 10
    ) -> RankingResult:
        """랭킹 조회

        Args:
            ranking_type: 랭킹 타입
            limit: 조회할 사용자 수

        Returns:
            RankingResult: 랭킹 결과
        """
        if ranking_type == RankingType.SCORE:
            users = await self.user_repo.get_ranking_by_score(limit)
        elif ranking_type == RankingType.CHAT_COUNT:
            users = await self.user_repo.get_ranking_by_chat_count(limit)
        elif ranking_type == RankingType.JACKPOT:
            users = await self.user_repo.get_ranking_by_jackpot(limit)
        elif ranking_type == RankingType.CONSECUTIVE_DAYS:
            users = await self.user_repo.get_ranking_by_consecutive_days(limit)
        else:
            users = []

        return RankingResult(ranking_type=ranking_type, users=users)
