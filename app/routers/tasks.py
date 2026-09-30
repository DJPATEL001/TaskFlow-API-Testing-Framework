import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
def get_tasks(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority_filter: Optional[str] = Query(None, alias="priority"),
    project_id: Optional[int] = Query(None),
    assigned_to: Optional[int] = Query(None),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve tasks with optional filtering and pagination."""
    query = db.query(Task)

    if current_user.role != "admin":
        # Non-admin users see tasks in projects they own or tasks assigned to them
        user_project_ids = [p.id for p in db.query(Project.id).filter(Project.owner_id == current_user.id).all()]
        query = query.filter((Task.project_id.in_(user_project_ids)) | (Task.assigned_to == current_user.id))

    if status_filter:
        query = query.filter(Task.status == status_filter)
    if priority_filter:
        query = query.filter(Task.priority == priority_filter)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)

    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 1
    offset = (page - 1) * limit
    tasks = query.offset(offset).limit(limit).all()

    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        limit=limit,
        pages=pages,
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task under an existing project."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == task_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with ID {task_data.project_id} does not exist",
        )

    # Verify assignee if specified
    if task_data.assigned_to:
        assignee = db.query(User).filter(User.id == task_data.assigned_to).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Assigned user with ID {task_data.assigned_to} does not exist",
            )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=task_data.status,
        project_id=task_data.project_id,
        assigned_to=task_data.assigned_to,
        due_date=task_data.due_date,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    update_dict = task_data.model_dump(exclude_unset=True)

    if "project_id" in update_dict and update_dict["project_id"] is not None:
        project = db.query(Project).filter(Project.id == update_dict["project_id"]).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project with ID {update_dict['project_id']} does not exist",
            )

    if "assigned_to" in update_dict and update_dict["assigned_to"] is not None:
        assignee = db.query(User).filter(User.id == update_dict["assigned_to"]).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Assigned user with ID {update_dict['assigned_to']} does not exist",
            )

    for field, value in update_dict.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    db.delete(task)
    db.commit()
    return None
