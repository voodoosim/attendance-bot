"""
Stats Service - 통계 서비스
"""
from datetime import date, datetime
from typing import Dict, Any

from src.core.use_cases.get_daily_stats_usecase import GetDailyStatsUseCase
from src.core.use_cases.get_monthly_stats_usecase import GetMonthlyStatsUseCase


class StatsService:
    """통계 서비스"""

    def __init__(
        self,
        daily_stats_usecase: GetDailyStatsUseCase,
        monthly_stats_usecase: GetMonthlyStatsUseCase,
    ):
        self.daily_stats_usecase = daily_stats_usecase
        self.monthly_stats_usecase = monthly_stats_usecase

    async def get_daily_stats(self, target_date: date = None) -> Dict[str, Any]:
        """일일 통계 조회 (기본값: 오늘)"""
        if target_date is None:
            target_date = datetime.now().date()

        return await self.daily_stats_usecase.execute(target_date)

    async def get_monthly_stats(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """월별 통계 조회 (기본값: 이번 달)"""
        now = datetime.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month

        return await self.monthly_stats_usecase.execute(year, month)
