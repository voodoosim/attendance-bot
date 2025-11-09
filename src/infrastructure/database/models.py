"""
Database models using SQLAlchemy
"""
from datetime import datetime
from typing import List

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    Float,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models"""

    pass


class UserModel(Base):
    """사용자 테이블"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    total_score: Mapped[int] = mapped_column(Integer, default=0, index=True)
    chat_count: Mapped[int] = mapped_column(Integer, default=0, index=True)
    jackpot_count: Mapped[int] = mapped_column(Integer, default=0)
    max_jackpot: Mapped[int] = mapped_column(Integer, default=0)
    consecutive_days: Mapped[int] = mapped_column(Integer, default=0)
    total_attendance: Mapped[int] = mapped_column(Integer, default=0)
    last_checkin: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    # Relationships
    attendances: Mapped[List["AttendanceModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    chat_activities: Mapped[List["ChatActivityModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, score={self.total_score})>"


class AttendanceModel(Base):
    """출석 기록 테이블"""

    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    consecutive_days: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    # Relationships
    user: Mapped["UserModel"] = relationship(back_populates="attendances")

    def __repr__(self) -> str:
        return f"<Attendance(user_id={self.user_id}, date={self.date}, score={self.score})>"


class ChatActivityModel(Base):
    """채팅 활동 테이블"""

    __tablename__ = "chat_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    base_score: Mapped[int] = mapped_column(Integer, nullable=False)
    is_jackpot: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    multiplier: Mapped[int] = mapped_column(Integer, default=1)
    final_score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), index=True)

    # Relationships
    user: Mapped["UserModel"] = relationship(back_populates="chat_activities")

    def __repr__(self) -> str:
        return (
            f"<ChatActivity(user_id={self.user_id}, "
            f"final_score={self.final_score}, jackpot={self.is_jackpot})>"
        )


class ScoreConfigModel(Base):
    """점수 설정 테이블"""

    __tablename__ = "score_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attendance_score: Mapped[int] = mapped_column(Integer, default=10)
    chat_score_min: Mapped[int] = mapped_column(Integer, default=1)
    chat_score_max: Mapped[int] = mapped_column(Integer, default=6)
    jackpot_chance: Mapped[float] = mapped_column(Float, default=0.05)
    multiplier_min: Mapped[int] = mapped_column(Integer, default=1)
    multiplier_max: Mapped[int] = mapped_column(Integer, default=7)
    max_consecutive_bonus: Mapped[int] = mapped_column(Integer, default=7)
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<ScoreConfig(id={self.id}, attendance={self.attendance_score})>"
