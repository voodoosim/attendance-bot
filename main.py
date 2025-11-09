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


# Configure logging
def setup_logging():
    """Configure application logging."""
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()
        ]
    )


async def main():
    """Main function to start the bot."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Attendance Bot...")

    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # TODO: Register handlers and middlewares
    # from src.handlers import register_handlers
    # register_handlers(dp)

    try:
        logger.info("Bot is running. Press Ctrl+C to stop.")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
