from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


TaskPriority = Literal["low", "medium", "high", "critical"]
TaskStatus = Literal["todo", "in_progress", "completed", "cancelled"]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Implement Auth Endpoints")
    description: Optional[str] = Field(None, example="Detailed task description")
    priority: TaskPriority = Field("medium", example="high")
    status: TaskStatus = Field("todo", example="in_progress")
    project_id: int = Field(..., example=1)
    assigned_to: Optional[int] = Field(None, example=2)
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    project_id: int
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    limit: int
    pages: int
