"""Reply keyboards for the bot."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Create main reply keyboard with action buttons.
    
    Returns:
        ReplyKeyboardMarkup with action buttons
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои задачи")],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="ℹ️ Помощь")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard
