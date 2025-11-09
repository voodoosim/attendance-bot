"""
Configuration module for Attendance Bot.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Bot Configuration
    bot_token: str = Field(..., description="Telegram Bot API token")
    admin_ids: str = Field(default="", description="Comma-separated admin user IDs")

    # Database Configuration
    database_url: str = Field(
        default="sqlite+aiosqlite:///./attendance.db",
        description="Database connection URL"
    )

    # Application Settings
    timezone: str = Field(default="Asia/Seoul", description="Application timezone")
    debug: bool = Field(default=False, description="Debug mode")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/bot.log", description="Log file path")

    @property
    def admin_list(self) -> List[int]:
        """Parse admin IDs from comma-separated string."""
        if not self.admin_ids:
            return []
        return [int(uid.strip()) for uid in self.admin_ids.split(",") if uid.strip()]


# Global settings instance
settings = Settings()
