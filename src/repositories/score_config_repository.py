"""
ScoreConfig Repository - Data access layer for ScoreConfig entity
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entities.score_config import ScoreConfig
from src.infrastructure.database.models import ScoreConfigModel


class ScoreConfigRepository:
    """점수 설정 저장소"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_config(self) -> ScoreConfig:
        """점수 설정 조회 (기본 ID=1)"""
        result = await self.session.execute(
            select(ScoreConfigModel).where(ScoreConfigModel.id == 1)
        )
        model = result.scalar_one_or_none()

        if not model:
            # 설정이 없으면 기본값 생성
            model = await self._create_default()

        return self._to_entity(model)

    async def update(self, config: ScoreConfig) -> ScoreConfig:
        """점수 설정 업데이트"""
        result = await self.session.execute(
            select(ScoreConfigModel).where(ScoreConfigModel.id == config.id)
        )
        model = result.scalar_one_or_none()

        if not model:
            # 없으면 생성
            model = ScoreConfigModel(
                id=config.id,
                attendance_score=config.attendance_score,
                chat_score_min=config.chat_score_min,
                chat_score_max=config.chat_score_max,
                jackpot_chance=config.jackpot_chance,
                multiplier_min=config.multiplier_min,
                multiplier_max=config.multiplier_max,
                max_consecutive_bonus=config.max_consecutive_bonus,
                updated_at=datetime.now(),
            )
            self.session.add(model)
        else:
            # 업데이트
            model.attendance_score = config.attendance_score
            model.chat_score_min = config.chat_score_min
            model.chat_score_max = config.chat_score_max
            model.jackpot_chance = config.jackpot_chance
            model.multiplier_min = config.multiplier_min
            model.multiplier_max = config.multiplier_max
            model.max_consecutive_bonus = config.max_consecutive_bonus
            model.updated_at = datetime.now()

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def _create_default(self) -> ScoreConfigModel:
        """기본 설정 생성"""
        model = ScoreConfigModel(
            id=1,
            attendance_score=10,
            chat_score_min=1,
            chat_score_max=6,
            jackpot_chance=0.05,
            multiplier_min=1,
            multiplier_max=7,
            max_consecutive_bonus=7,
            updated_at=datetime.now(),
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    def _to_entity(self, model: ScoreConfigModel) -> ScoreConfig:
        """모델을 엔티티로 변환"""
        return ScoreConfig(
            id=model.id,
            attendance_score=model.attendance_score,
            chat_score_min=model.chat_score_min,
            chat_score_max=model.chat_score_max,
            jackpot_chance=model.jackpot_chance,
            multiplier_min=model.multiplier_min,
            multiplier_max=model.multiplier_max,
            max_consecutive_bonus=model.max_consecutive_bonus,
            updated_at=model.updated_at,
        )
