"""Inline keyboards for the bot."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def get_webapp_keyboard(web_app_url: str) -> InlineKeyboardMarkup:
    """
    Create keyboard with Web App button.
    
    Args:
        web_app_url: URL of the web application
        
    Returns:
        InlineKeyboardMarkup with Web App button
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Open Task Manager",
                    web_app=WebAppInfo(url=web_app_url)
                )
            ]
        ]
    )
    return keyboard


def get_task_actions_keyboard(task_id: int) -> InlineKeyboardMarkup:
    """
    Create keyboard with task action buttons.
    
    Args:
        task_id: ID of the task
        
    Returns:
        InlineKeyboardMarkup with action buttons
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Mark as Done",
                    callback_data=f"task_done:{task_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 Delete",
                    callback_data=f"task_delete:{task_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏸ In Progress",
                    callback_data=f"task_progress:{task_id}"
                ),
                InlineKeyboardButton(
                    text="↩️ To Do",
                    callback_data=f"task_todo:{task_id}"
                )
            ]
        ]
    )
    return keyboard


def get_confirm_keyboard(action: str, task_id: int) -> InlineKeyboardMarkup:
    """
    Create confirmation keyboard.
    
    Args:
        action: Action to confirm
        task_id: ID of the task
        
    Returns:
        InlineKeyboardMarkup with confirmation buttons
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Yes",
                    callback_data=f"confirm_{action}:{task_id}"
                ),
                InlineKeyboardButton(
                    text="❌ No",
                    callback_data=f"cancel_{action}:{task_id}"
                )
            ]
        ]
    )
    return keyboard
