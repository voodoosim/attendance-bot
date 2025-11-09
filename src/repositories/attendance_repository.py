"""
Attendance Repository - Data access layer for Attendance entity
"""
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.attendance import Attendance
from src.infrastructure.database.models import AttendanceModel


class AttendanceRepository:
    """출석 기록 저장소"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_and_date(
        self, user_id: int, attendance_date: date
    ) -> Optional[Attendance]:
        """사용자와 날짜로 출석 기록 조회"""
        result = await self.session.execute(
            select(AttendanceModel).where(
                AttendanceModel.user_id == user_id,
                AttendanceModel.date == attendance_date,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_user(self, user_id: int, limit: int = 30) -> List[Attendance]:
        """사용자의 출석 기록 조회 (최근 N일)"""
        result = await self.session.execute(
            select(AttendanceModel)
            .where(AttendanceModel.user_id == user_id)
            .order_by(AttendanceModel.date.desc())
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def create(
        self, user_id: int, attendance_date: date, score: int, consecutive_days: int
    ) -> Attendance:
        """출석 기록 생성"""
        model = AttendanceModel(
            user_id=user_id,
            date=attendance_date,
            score=score,
            consecutive_days=consecutive_days,
            created_at=datetime.now(),
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_total_count(self, user_id: int) -> int:
        """사용자의 총 출석 횟수"""
        result = await self.session.execute(
            select(AttendanceModel).where(AttendanceModel.user_id == user_id)
        )
        return len(result.scalars().all())

    def _to_entity(self, model: AttendanceModel) -> Attendance:
        """모델을 엔티티로 변환"""
        return Attendance(
            id=model.id,
            user_id=model.user_id,
            date=model.date,
            score=model.score,
            consecutive_days=model.consecutive_days,
            created_at=model.created_at,
        )
