"""
Main entry point for Attendance Bot.
"""
import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from src.infrastructure.database.connection import db_manager

# Repositories
from src.repositories.user_repository import UserRepository
from src.repositories.attendance_repository import AttendanceRepository
from src.repositories.chat_activity_repository import ChatActivityRepository
from src.repositories.score_config_repository import ScoreConfigRepository

# Use Cases
from src.core.use_cases.check_in_usecase import CheckInUseCase
from src.core.use_cases.process_message_usecase import ProcessMessageUseCase
from src.core.use_cases.get_user_info_usecase import GetUserInfoUseCase
from src.core.use_cases.get_ranking_usecase import GetRankingUseCase
from src.core.use_cases.get_daily_stats_usecase import GetDailyStatsUseCase
from src.core.use_cases.get_monthly_stats_usecase import GetMonthlyStatsUseCase

# Services
from src.services.attendance_service import AttendanceService
from src.services.chat_activity_service import ChatActivityService
from src.services.user_service import UserService
from src.services.stats_service import StatsService

# Handlers
from src.handlers import (
    start_handler,
    check_in_handler,
    message_handler,
    user_info_handler,
    ranking_handler,
    stats_handler,
)


# Configure logging
def setup_logging():
    """Configure application logging."""
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(settings.log_file), logging.StreamHandler()],
    )


async def setup_dependencies(dp: Dispatcher):
    """Setup dependency injection"""

    async def get_services():
        """Create services with repositories"""
        async with db_manager.session() as session:
            # Repositories
            user_repo = UserRepository(session)
            attendance_repo = AttendanceRepository(session)
            chat_activity_repo = ChatActivityRepository(session)
            config_repo = ScoreConfigRepository(session)

            # Use Cases
            checkin_usecase = CheckInUseCase(user_repo, attendance_repo, config_repo)
            process_message_usecase = ProcessMessageUseCase(
                user_repo, chat_activity_repo, config_repo
            )
            get_user_info_usecase = GetUserInfoUseCase(
                user_repo, attendance_repo, chat_activity_repo
            )
            get_ranking_usecase = GetRankingUseCase(user_repo)
            daily_stats_usecase = GetDailyStatsUseCase(
                user_repo, attendance_repo, chat_activity_repo
            )
            monthly_stats_usecase = GetMonthlyStatsUseCase(
                user_repo, attendance_repo, chat_activity_repo
            )

            # Services
            attendance_service = AttendanceService(checkin_usecase)
            chat_activity_service = ChatActivityService(process_message_usecase)
            user_service = UserService(get_user_info_usecase, get_ranking_usecase)
            stats_service = StatsService(daily_stats_usecase, monthly_stats_usecase)

            return {
                "attendance_service": attendance_service,
                "chat_activity_service": chat_activity_service,
                "user_service": user_service,
                "stats_service": stats_service,
            }

    # Store services factory in dispatcher
    dp["get_services"] = get_services


def register_handlers(dp: Dispatcher):
    """Register all message handlers"""
    # Order matters: specific before general
    dp.include_router(start_handler.router)
    dp.include_router(check_in_handler.router)
    dp.include_router(user_info_handler.router)
    dp.include_router(ranking_handler.router)
    dp.include_router(stats_handler.router)
    dp.include_router(message_handler.router)  # General message handler last


async def on_startup():
    """Initialize database on startup"""
    logger = logging.getLogger(__name__)
    logger.info("Initializing database...")
    await db_manager.init_db()
    logger.info("Database initialized successfully")


async def on_shutdown():
    """Close database connection on shutdown"""
    logger = logging.getLogger(__name__)
    logger.info("Closing database connection...")
    await db_manager.close()
    logger.info("Database connection closed")


async def main():
    """Main function to start the bot."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Attendance Bot...")

    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Setup dependencies and handlers
    await setup_dependencies(dp)
    register_handlers(dp)

    # Startup
    await on_startup()

    try:
        logger.info("Bot is running. Press Ctrl+C to stop.")

        # Middleware to inject services
        @dp.update.outer_middleware()
        async def services_middleware(handler, event, data):
            get_services = dp["get_services"]
            services = await get_services()
            data.update(services)
            return await handler(event, data)

        await dp.start_polling(bot)
    finally:
        await on_shutdown()
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
