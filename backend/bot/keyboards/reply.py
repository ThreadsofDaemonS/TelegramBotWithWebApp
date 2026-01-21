"""Reply keyboards for the bot."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from bot.config import config


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Main keyboard with WebApp button (blue button at bottom of chat).
    
    Returns:
        ReplyKeyboardMarkup with WebApp button and quick action buttons
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="📱 Открыть Task Tracker",
                web_app=WebAppInfo(url=config.webapp_url)
            )],
            [
                KeyboardButton(text="📋 Мои задачи"),
                KeyboardButton(text="📊 Статистика")
            ],
            [KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard
