from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.schemas.dashboard import DashboardResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get project and task statistics dashboard."""
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    pending_tasks = db.query(Task).filter(Task.status.in_(["todo", "in_progress"])).count()
    high_priority_tasks = db.query(Task).filter(Task.priority.in_(["high", "critical"])).count()

    return DashboardResponse(
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        high_priority_tasks=high_priority_tasks,
    )
