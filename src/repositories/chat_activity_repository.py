"""
ChatActivity Repository - Data access layer for ChatActivity entity
"""
from datetime import datetime
from typing import List

from sqlalchemy import select
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
