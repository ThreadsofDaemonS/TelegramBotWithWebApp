"""Bot main entry point."""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.handlers import start, tasks
from bot.middlewares import DatabaseMiddleware
from database import close_db, init_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main bot function."""
    # Initialize bot and dispatcher
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Register middlewares
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(tasks.router)
    
    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)
    
    # Set webhook
    if config.webhook_url:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.set_webhook(
                url=config.webhook_url,
                allowed_updates=dp.resolve_used_update_types(),
                drop_pending_updates=True
            )
            logger.info(f"Webhook set to: {config.webhook_url}")
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            sys.exit(1)
    else:
        logger.warning("WEBHOOK_URL not set, bot will not receive updates")
    
    # Keep bot running
    logger.info("Bot started successfully")
    try:
        # Keep alive - webhook mode doesn't need polling
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopping...")
    finally:
        await bot.session.close()
        await close_db()
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
