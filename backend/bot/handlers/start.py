"""Start command handler."""
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import get_main_keyboard
from database.models import User

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession) -> None:
    """
    Handle /start command.
    
    Creates user in database if not exists and shows welcome message with reply keyboard.
    
    Args:
        message: Telegram message
        session: Database session
    """
    try:
        user_telegram_id = message.from_user.id
        
        # Check if user exists
        result = await session.execute(
            select(User).where(User.telegram_id == user_telegram_id)
        )
        user = result.scalar_one_or_none()
        
        # Create user if not exists
        if not user:
            user = User(
                telegram_id=user_telegram_id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
            session.add(user)
            await session.commit()
            logger.info(f"Created new user: {user_telegram_id}")
        
        # Send welcome message with instructions to use Menu Button
        welcome_text = (
            "👋 Добро пожаловать в Task Tracker!\n\n"
            "📱 Нажмите кнопку «Открыть» слева от поля ввода\n"
            "для запуска приложения\n\n"
            "Или выберите действие из меню ниже:"
        )
        
        await message.answer(
            welcome_text,
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in start handler: {e}", exc_info=True)
        await message.answer(
            "❌ Sorry, something went wrong. Please try again later."
        )
