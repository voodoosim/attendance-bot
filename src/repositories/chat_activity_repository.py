"""
ChatActivity Repository - Data access layer for ChatActivity entity
"""
from datetime import datetime, date
from typing import List, Optional, Tuple

from sqlalchemy import select, func, cast, Date, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.chat_activity import ChatActivity
from src.infrastructure.database.models import ChatActivityModel


class ChatActivityRepository:
    """채팅 활동 저장소"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, activity: ChatActivity) -> ChatActivity:
        """채팅 활동 생성"""
        model = ChatActivityModel(
            user_id=activity.user_id,
            message_id=activity.message_id,
            base_score=activity.base_score,
            is_jackpot=activity.is_jackpot,
            multiplier=activity.multiplier,
            final_score=activity.final_score,
            created_at=activity.created_at,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_user(self, user_id: int, limit: int = 100) -> List[ChatActivity]:
        """사용자의 채팅 활동 조회 (최근 N개)"""
        result = await self.session.execute(
            select(ChatActivityModel)
            .where(ChatActivityModel.user_id == user_id)
            .order_by(ChatActivityModel.created_at.desc())
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_jackpots_by_user(self, user_id: int, limit: int = 10) -> List[ChatActivity]:
        """사용자의 잭팟 기록 조회"""
        result = await self.session.execute(
            select(ChatActivityModel)
            .where(
                ChatActivityModel.user_id == user_id,
                ChatActivityModel.is_jackpot == True,  # noqa: E712
            )
            .order_by(ChatActivityModel.final_score.desc())
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_daily_stats(
        self, target_date: date
    ) -> Tuple[int, int, int, int]:
        """일일 채팅 통계 (메시지 수, 총 점수, 잭팟 횟수, 활동 사용자 수)"""
        result = await self.session.execute(
            select(
                func.count(ChatActivityModel.id),
                func.sum(ChatActivityModel.final_score),
                func.count(ChatActivityModel.id).filter(ChatActivityModel.is_jackpot == True),  # noqa: E712
                func.count(func.distinct(ChatActivityModel.user_id)),
            ).where(cast(ChatActivityModel.created_at, Date) == target_date)
        )
        row = result.one()
        return (
            row[0] or 0,  # 메시지 수
            row[1] or 0,  # 총 점수
            row[2] or 0,  # 잭팟 횟수
            row[3] or 0,  # 활동 사용자 수
        )

    async def get_monthly_stats(
        self, year: int, month: int
    ) -> Tuple[int, int, int, int]:
        """월별 채팅 통계 (메시지 수, 총 점수, 잭팟 횟수, 활동 사용자 수)"""
        result = await self.session.execute(
            select(
                func.count(ChatActivityModel.id),
                func.sum(ChatActivityModel.final_score),
                func.count(ChatActivityModel.id).filter(ChatActivityModel.is_jackpot == True),  # noqa: E712
                func.count(func.distinct(ChatActivityModel.user_id)),
            ).where(
                extract("year", ChatActivityModel.created_at) == year,
                extract("month", ChatActivityModel.created_at) == month,
            )
        )
        row = result.one()
        return (
            row[0] or 0,  # 메시지 수
            row[1] or 0,  # 총 점수
            row[2] or 0,  # 잭팟 횟수
            row[3] or 0,  # 활동 사용자 수
        )

    async def get_most_active_date(
        self, year: int, month: int
    ) -> Optional[Tuple[date, int]]:
        """가장 활발했던 날과 그 날의 메시지 수"""
        result = await self.session.execute(
            select(
                cast(ChatActivityModel.created_at, Date),
                func.count(ChatActivityModel.id),
            )
            .where(
                extract("year", ChatActivityModel.created_at) == year,
                extract("month", ChatActivityModel.created_at) == month,
            )
            .group_by(cast(ChatActivityModel.created_at, Date))
            .order_by(func.count(ChatActivityModel.id).desc())
            .limit(1)
        )
        row = result.one_or_none()
        return row if row else None

    def _to_entity(self, model: ChatActivityModel) -> ChatActivity:
        """모델을 엔티티로 변환"""
        return ChatActivity(
            id=model.id,
            user_id=model.user_id,
            message_id=model.message_id,
            base_score=model.base_score,
            is_jackpot=model.is_jackpot,
            multiplier=model.multiplier,
            final_score=model.final_score,
            created_at=model.created_at,
        )
