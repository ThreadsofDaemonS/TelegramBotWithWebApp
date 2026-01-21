"""Task-related command handlers."""
import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import get_main_keyboard, get_task_actions_keyboard
from database.models import Task, TaskPriority, TaskStatus, User

router = Router()
logger = logging.getLogger(__name__)


class AddTaskStates(StatesGroup):
    """States for adding a task."""
    waiting_for_title = State()


@router.message(Command("mytasks"))
async def cmd_my_tasks(message: Message, session: AsyncSession) -> None:
    """
    Handle /mytasks command - show user's tasks summary.
    
    Args:
        message: Telegram message
        session: Database session
    """
    try:
        user_telegram_id = message.from_user.id
        
        # Get user
        result = await session.execute(
            select(User).where(User.telegram_id == user_telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("❌ User not found. Please use /start first.")
            return
        
        # Get task statistics
        result = await session.execute(
            select(
                func.count(Task.id).label("total"),
                func.sum(func.cast(Task.status == TaskStatus.TODO, type_=type(1))).label("todo"),
                func.sum(func.cast(Task.status == TaskStatus.IN_PROGRESS, type_=type(1))).label("in_progress"),
                func.sum(func.cast(Task.status == TaskStatus.DONE, type_=type(1))).label("done"),
            ).where(Task.user_id == user.id)
        )
        stats = result.one()
        
        # Get recent tasks
        result = await session.execute(
            select(Task)
            .where(Task.user_id == user.id)
            .where(Task.status != TaskStatus.DONE)
            .order_by(Task.priority.desc(), Task.created_at.desc())
            .limit(5)
        )
        recent_tasks = result.scalars().all()
        
        # Format response
        response_text = "📊 **Your Tasks Summary**\n\n"
        response_text += f"📝 Total: {stats.total or 0}\n"
        response_text += f"⏳ To Do: {stats.todo or 0}\n"
        response_text += f"🔄 In Progress: {stats.in_progress or 0}\n"
        response_text += f"✅ Done: {stats.done or 0}\n\n"
        
        if recent_tasks:
            response_text += "**Recent Tasks:**\n\n"
            for task in recent_tasks:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                status_emoji = {"todo": "⏳", "in_progress": "🔄", "done": "✅"}
                
                response_text += (
                    f"{priority_emoji.get(task.priority.value, '⚪')} "
                    f"{status_emoji.get(task.status.value, '⚪')} "
                    f"**{task.title}**\n"
                )
        else:
            response_text += "No active tasks. Use /addtask to create one!"
        
        await message.answer(response_text, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error in mytasks handler: {e}", exc_info=True)
        await message.answer("❌ Error fetching tasks. Please try again.")


@router.message(F.text == "📋 Мои задачи")
async def show_my_tasks(message: Message, session: AsyncSession) -> None:
    """
    Handle '📋 Мои задачи' button - show user's tasks summary.
    
    Args:
        message: Telegram message
        session: Database session
    """
    try:
        user_telegram_id = message.from_user.id
        
        # Get user
        result = await session.execute(
            select(User).where(User.telegram_id == user_telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("❌ Пользователь не найден. Используйте /start.")
            return
        
        # Get task statistics
        result = await session.execute(
            select(
                func.count(Task.id).label("total"),
                func.sum(func.cast(Task.status == TaskStatus.TODO, type_=type(1))).label("todo"),
                func.sum(func.cast(Task.status == TaskStatus.IN_PROGRESS, type_=type(1))).label("in_progress"),
                func.sum(func.cast(Task.status == TaskStatus.DONE, type_=type(1))).label("done"),
            ).where(Task.user_id == user.id)
        )
        stats = result.one()
        
        # Format response
        response_text = "📋 Ваши задачи:\n\n"
        response_text += f"⏳ К выполнению: {stats.todo or 0}\n"
        response_text += f"🔵 В работе: {stats.in_progress or 0}\n"
        response_text += f"✅ Завершено: {stats.done or 0}\n"
        response_text += f"📝 Всего: {stats.total or 0}\n\n"
        response_text += "Откройте приложение для подробностей 👇"
        
        await message.answer(
            response_text,
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in show_my_tasks handler: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении задач.")


@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message, session: AsyncSession) -> None:
    """
    Handle '📊 Статистика' button - show user statistics.
    
    Args:
        message: Telegram message
        session: Database session
    """
    try:
        user_telegram_id = message.from_user.id
        
        # Get user
        result = await session.execute(
            select(User).where(User.telegram_id == user_telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("❌ Пользователь не найден. Используйте /start.")
            return
        
        # Get task statistics
        result = await session.execute(
            select(
                func.count(Task.id).label("total"),
                func.sum(func.cast(Task.status == TaskStatus.DONE, type_=type(1))).label("done"),
            ).where(Task.user_id == user.id)
        )
        stats = result.one()
        
        # For now, just show basic stats
        # TODO: Implement streak calculation based on task completion dates
        response_text = "📊 Ваша статистика:\n\n"
        response_text += f"🎯 Задач создано: {stats.total or 0}\n"
        response_text += f"✅ Задач выполнено: {stats.done or 0}\n"
        response_text += f"🔥 Серия дней: 0\n"
        
        await message.answer(
            response_text,
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Error in show_statistics handler: {e}", exc_info=True)
        await message.answer("❌ Ошибка при получении статистики.")


@router.message(F.text == "ℹ️ Помощь")
async def show_help(message: Message) -> None:
    """
    Handle 'ℹ️ Помощь' button - show help information.
    
    Args:
        message: Telegram message
    """
    help_text = (
        "ℹ️ Помощь по боту:\n\n"
        "/start - Начать работу\n"
        "/mytasks - Мои задачи\n"
        "/addtask - Создать задачу\n\n"
        "📱 Используйте Web App для полного функционала!"
    )
    await message.answer(
        help_text,
        reply_markup=get_main_keyboard()
    )


@router.message(Command("addtask"))
async def cmd_add_task(message: Message, state: FSMContext) -> None:
    """
    Handle /addtask command - start task creation process.
    
    Args:
        message: Telegram message
        state: FSM context
    """
    await message.answer(
        "📝 **Add New Task**\n\n"
        "Please send me the task title:\n"
        "(Send /cancel to abort)"
    )
    await state.set_state(AddTaskStates.waiting_for_title)


@router.message(AddTaskStates.waiting_for_title, F.text)
async def process_task_title(message: Message, state: FSMContext, session: AsyncSession) -> None:
    """
    Process task title and create task.
    
    Args:
        message: Telegram message
        state: FSM context
        session: Database session
    """
    try:
        if message.text == "/cancel":
            await state.clear()
            await message.answer("❌ Task creation cancelled.")
            return
        
        user_telegram_id = message.from_user.id
        
        # Get user
        result = await session.execute(
            select(User).where(User.telegram_id == user_telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("❌ User not found. Please use /start first.")
            await state.clear()
            return
        
        # Create task
        task = Task(
            user_id=user.id,
            title=message.text,
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
        )
        session.add(task)
        await session.commit()
        
        await message.answer(
            f"✅ Task created successfully!\n\n"
            f"**{task.title}**\n"
            f"Status: To Do\n"
            f"Priority: Medium",
            reply_markup=get_task_actions_keyboard(task.id),
            parse_mode="Markdown"
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error creating task: {e}", exc_info=True)
        await message.answer("❌ Error creating task. Please try again.")
        await state.clear()


@router.callback_query(F.data.startswith("task_"))
async def handle_task_action(callback: CallbackQuery, session: AsyncSession) -> None:
    """
    Handle task action callbacks.
    
    Args:
        callback: Callback query
        session: Database session
    """
    try:
        action, task_id = callback.data.split(":")
        task_id = int(task_id)
        
        # Get task
        result = await session.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            await callback.answer("❌ Task not found.")
            return
        
        # Verify user owns the task
        result = await session.execute(
            select(User).where(User.id == task.user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user or user.telegram_id != callback.from_user.id:
            await callback.answer("❌ You don't have permission for this task.")
            return
        
        # Perform action
        if action == "task_done":
            task.status = TaskStatus.DONE
            status_text = "✅ marked as done"
        elif action == "task_progress":
            task.status = TaskStatus.IN_PROGRESS
            status_text = "🔄 moved to in progress"
        elif action == "task_todo":
            task.status = TaskStatus.TODO
            status_text = "⏳ moved to to do"
        elif action == "task_delete":
            await session.delete(task)
            await session.commit()
            await callback.message.edit_text(
                f"🗑 Task deleted:\n~~{task.title}~~",
                parse_mode="Markdown"
            )
            await callback.answer("Task deleted!")
            return
        else:
            await callback.answer("❌ Unknown action.")
            return
        
        task.updated_at = datetime.utcnow()
        await session.commit()
        
        await callback.message.edit_text(
            f"Task {status_text}!\n\n**{task.title}**",
            reply_markup=get_task_actions_keyboard(task.id),
            parse_mode="Markdown"
        )
        await callback.answer(f"Task {status_text}!")
        
    except Exception as e:
        logger.error(f"Error handling task action: {e}", exc_info=True)
        await callback.answer("❌ Error processing action.")
