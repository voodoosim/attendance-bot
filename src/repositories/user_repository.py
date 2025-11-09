"""
User Repository - Data access layer for User entity
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.user import User
from src.infrastructure.database.models import UserModel


class UserRepository:
    """사용자 저장소"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Telegram ID로 사용자 조회"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def create(self, telegram_id: int, username: str) -> User:
        """사용자 생성"""
        model = UserModel(
            telegram_id=telegram_id,
            username=username,
            total_score=0,
            chat_count=0,
            jackpot_count=0,
            max_jackpot=0,
            consecutive_days=0,
            total_attendance=0,
            last_checkin=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        """사용자 업데이트"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one()

        model.username = user.username
        model.total_score = user.total_score
        model.chat_count = user.chat_count
        model.jackpot_count = user.jackpot_count
        model.max_jackpot = user.max_jackpot
        model.consecutive_days = user.consecutive_days
        model.total_attendance = user.total_attendance
        model.last_checkin = user.last_checkin
        model.updated_at = datetime.now()

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_ranking_by_score(self, limit: int = 10) -> List[User]:
        """점수 순위 조회"""
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.total_score > 0)
            .order_by(UserModel.total_score.desc())
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_ranking_by_chat_count(self, limit: int = 10) -> List[User]:
        """채팅 수 순위 조회"""
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.chat_count > 0)
            .order_by(UserModel.chat_count.desc())
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_ranking_by_jackpot(self, limit: int = 10) -> List[User]:
        """잭팟 횟수 순위 조회"""
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.jackpot_count > 0)
            .order_by(UserModel.jackpot_count.desc(), UserModel.max_jackpot.desc())
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_ranking_by_consecutive_days(self, limit: int = 10) -> List[User]:
        """연속 출석일 순위 조회"""
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.consecutive_days > 0)
            .order_by(UserModel.consecutive_days.desc(), UserModel.total_attendance.desc())
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    def _to_entity(self, model: UserModel) -> User:
        """모델을 엔티티로 변환"""
        return User(
            id=model.id,
            telegram_id=model.telegram_id,
            username=model.username,
            total_score=model.total_score,
            chat_count=model.chat_count,
            jackpot_count=model.jackpot_count,
            max_jackpot=model.max_jackpot,
            consecutive_days=model.consecutive_days,
            total_attendance=model.total_attendance,
            last_checkin=model.last_checkin,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
