"""
Statistics Entities
"""
from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class UserStats:
    """개별 사용자 통계"""

    telegram_id: int
    username: str
    total_score: int
    chat_count: int


@dataclass
class DailyStats:
    """일일 통계"""

    date: date
    total_users: int  # 오늘 활동한 사용자 수
    check_in_count: int  # 오늘 출석한 사람 수
    total_messages: int  # 오늘 총 채팅 수
    total_score: int  # 오늘 총 획득 점수
    jackpot_count: int  # 오늘 잭팟 횟수
    top_users: List[UserStats]  # 오늘 TOP 사용자


@dataclass
class MonthlyStats:
    """월별 통계"""

    year: int
    month: int
    total_users: int  # 이번 달 활동 사용자 수
    check_in_count: int  # 이번 달 총 출석 횟수
    total_messages: int  # 이번 달 총 채팅 수
    total_score: int  # 이번 달 총 획득 점수
    jackpot_count: int  # 이번 달 잭팟 횟수
    most_active_date: Optional[date]  # 가장 활발했던 날
    most_active_count: int  # 가장 활발했던 날의 채팅 수
    top_users: List[UserStats]  # 이번 달 TOP 사용자
