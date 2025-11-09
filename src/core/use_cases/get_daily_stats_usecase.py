"""
Get Daily Stats Use Case - 일일 통계 조회
"""
from datetime import date
from typing import Dict, Any

from src.core.entities.stats import DailyStats, UserStats
from src.repositories.user_repository import UserRepository
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.chat_activity_repository import ChatActivityRepository


class GetDailyStatsUseCase:
    """일일 통계 조회 유스케이스"""

    def __init__(
        self,
        user_repo: UserRepository,
        attendance_repo: AttendanceRepository,
        chat_activity_repo: ChatActivityRepository,
    ):
        self.user_repo = user_repo
        self.attendance_repo = attendance_repo
        self.chat_activity_repo = chat_activity_repo

    async def execute(self, target_date: date) -> Dict[str, Any]:
        """일일 통계 조회 실행"""
        # 1. 출석 횟수
        check_in_count = await self.attendance_repo.get_daily_count(target_date)

        # 2. 채팅 통계 (메시지 수, 총 점수, 잭팟 횟수, 활동 사용자 수)
        (
            total_messages,
            total_score,
            jackpot_count,
            total_users,
        ) = await self.chat_activity_repo.get_daily_stats(target_date)

        # 3. TOP 사용자 (점수 기준 TOP 3)
        top_users_models = await self.user_repo.get_ranking_by_score(limit=3)
        top_users = [
            UserStats(
                telegram_id=user.telegram_id,
                username=user.username,
                total_score=user.total_score,
                chat_count=user.chat_count,
            )
            for user in top_users_models
        ]

        # 4. DailyStats 엔티티 생성
        daily_stats = DailyStats(
            date=target_date,
            total_users=total_users,
            check_in_count=check_in_count,
            total_messages=total_messages,
            total_score=total_score,
            jackpot_count=jackpot_count,
            top_users=top_users,
        )

        return {"success": True, "stats": daily_stats}
