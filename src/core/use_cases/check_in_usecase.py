"""
CheckIn Use Case - 출석 체크 비즈니스 로직
"""
from dataclasses import dataclass
from datetime import datetime

from src.core.entities.attendance import Attendance
from src.core.entities.user import User
from src.core.exceptions import AlreadyCheckedInError
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.score_config_repository import ScoreConfigRepository
from src.repositories.user_repository import UserRepository


@dataclass
class CheckInResult:
    """출석 체크 결과"""

    user: User
    attendance: Attendance
    score: int
    consecutive_days: int
    is_new_user: bool


class CheckInUseCase:
    """출석 체크 유스케이스"""

    def __init__(
        self,
        user_repo: UserRepository,
        attendance_repo: AttendanceRepository,
        config_repo: ScoreConfigRepository,
    ):
        self.user_repo = user_repo
        self.attendance_repo = attendance_repo
        self.config_repo = config_repo

    async def execute(self, telegram_id: int, username: str) -> CheckInResult:
        """출석 체크 실행

        Args:
            telegram_id: 텔레그램 사용자 ID
            username: 사용자 이름

        Returns:
            CheckInResult: 출석 체크 결과

        Raises:
            AlreadyCheckedInError: 이미 오늘 출석한 경우
        """
        # 1. 사용자 조회 또는 생성
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        is_new_user = False

        if not user:
            user = await self.user_repo.create(telegram_id, username)
            is_new_user = True

        # 2. 오늘 출석 가능 여부 확인
        if not user.can_checkin_today():
            raise AlreadyCheckedInError("이미 오늘 출석했습니다!")

        # 3. 연속 출석일 계산
        consecutive_days = user.calculate_consecutive_days()

        # 4. 출석 점수 계산
        config = await self.config_repo.get_config()
        score = Attendance.calculate_score(
            base_score=config.attendance_score,
            consecutive_days=consecutive_days,
            max_bonus=config.max_consecutive_bonus,
        )

        # 5. 출석 기록 저장
        attendance = await self.attendance_repo.create(
            user_id=user.id,
            attendance_date=datetime.now().date(),
            score=score,
            consecutive_days=consecutive_days,
        )

        # 6. 사용자 정보 업데이트
        user.add_score(score)
        user.update_checkin(consecutive_days)
        await self.user_repo.update(user)

        return CheckInResult(
            user=user,
            attendance=attendance,
            score=score,
            consecutive_days=consecutive_days,
            is_new_user=is_new_user,
        )
