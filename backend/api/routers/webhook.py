"""
Webhook router - NOT USED in polling mode (local development)
Only needed for production deployment with webhook
"""
# This router is disabled for local development
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import APIRouter, Request

from api.config import config
from bot.handlers import start, tasks
from bot.middlewares import DatabaseMiddleware

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher (shared instance)
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


@router.post("/webhook")
async def webhook_handler(request: Request) -> dict:
    """
    Handle incoming webhook updates from Telegram.
    
    Args:
        request: FastAPI request
        
    Returns:
        dict: Status response
    """
    try:
        # Get update from request body
        update_dict = await request.json()
        update = Update(**update_dict)
        
        # Feed update to dispatcher
        await dp.feed_update(bot=bot, update=update)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
