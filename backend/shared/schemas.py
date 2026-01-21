"""Shared Pydantic schemas for data validation and serialization."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from database.models import TaskPriority, TaskStatus


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    pass


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Task Schemas
class TaskBase(BaseModel):
    """Base task schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    user_id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Statistics Schema
class TaskStatsResponse(BaseModel):
    """Schema for task statistics response."""
    total: int
    todo: int
    in_progress: int
    done: int
    high_priority: int
    medium_priority: int
    low_priority: int
