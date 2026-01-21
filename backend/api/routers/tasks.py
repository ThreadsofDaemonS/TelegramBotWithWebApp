"""Tasks router for CRUD operations on tasks."""
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import get_current_user
from api.dependencies import get_session
from database.models import Task, TaskPriority, TaskStatus, User
from shared.schemas import TaskCreate, TaskResponse, TaskStatsResponse, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])
logger = logging.getLogger(__name__)


async def get_user_by_telegram_id(
    telegram_id: int,
    session: AsyncSession
) -> User:
    """
    Get user by Telegram ID or raise 404.
    
    Args:
        telegram_id: Telegram user ID
        session: Database session
        
    Returns:
        User: User object
        
    Raises:
        HTTPException: If user not found
    """
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
) -> List[Task]:
    """
    Get list of user's tasks.
    
    Args:
        status: Filter by status (optional)
        priority: Filter by priority (optional)
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        List[Task]: List of tasks
    """
    try:
        # Get user
        user = await get_user_by_telegram_id(current_user["id"], session)
        
        # Build query
        query = select(Task).where(Task.user_id == user.id)
        
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        
        query = query.order_by(Task.created_at.desc())
        
        result = await session.execute(query)
        tasks = result.scalars().all()
        
        return tasks
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing tasks: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching tasks")


@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
) -> Task:
    """
    Create a new task.
    
    Args:
        task_data: Task creation data
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        Task: Created task
    """
    try:
        # Get user
        user = await get_user_by_telegram_id(current_user["id"], session)
        
        # Create task
        task = Task(
            user_id=user.id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            deadline=task_data.deadline,
            status=TaskStatus.TODO,
        )
        
        session.add(task)
        await session.commit()
        await session.refresh(task)
        
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error creating task")


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
) -> Task:
    """
    Update a task.
    
    Args:
        task_id: Task ID
        task_data: Task update data
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        Task: Updated task
    """
    try:
        # Get user
        user = await get_user_by_telegram_id(current_user["id"], session)
        
        # Get task
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user.id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        await session.commit()
        await session.refresh(task)
        
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error updating task")


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Delete a task.
    
    Args:
        task_id: Task ID
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        dict: Status message
    """
    try:
        # Get user
        user = await get_user_by_telegram_id(current_user["id"], session)
        
        # Get task
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user.id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        await session.delete(task)
        await session.commit()
        
        return {"status": "success", "message": "Task deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error deleting task")


@router.get("/stats", response_model=TaskStatsResponse)
async def get_task_stats(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
) -> TaskStatsResponse:
    """
    Get user's task statistics.
    
    Args:
        session: Database session
        current_user: Current authenticated user
        
    Returns:
        TaskStatsResponse: Task statistics
    """
    try:
        # Get user
        user = await get_user_by_telegram_id(current_user["id"], session)
        
        # Get statistics
        result = await session.execute(
            select(
                func.count(Task.id).label("total"),
                func.sum(func.cast(Task.status == TaskStatus.TODO, type_=type(1))).label("todo"),
                func.sum(func.cast(Task.status == TaskStatus.IN_PROGRESS, type_=type(1))).label("in_progress"),
                func.sum(func.cast(Task.status == TaskStatus.DONE, type_=type(1))).label("done"),
                func.sum(func.cast(Task.priority == TaskPriority.HIGH, type_=type(1))).label("high_priority"),
                func.sum(func.cast(Task.priority == TaskPriority.MEDIUM, type_=type(1))).label("medium_priority"),
                func.sum(func.cast(Task.priority == TaskPriority.LOW, type_=type(1))).label("low_priority"),
            ).where(Task.user_id == user.id)
        )
        stats = result.one()
        
        return TaskStatsResponse(
            total=stats.total or 0,
            todo=stats.todo or 0,
            in_progress=stats.in_progress or 0,
            done=stats.done or 0,
            high_priority=stats.high_priority or 0,
            medium_priority=stats.medium_priority or 0,
            low_priority=stats.low_priority or 0,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching statistics")
