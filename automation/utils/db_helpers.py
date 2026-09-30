from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.project import Project
from app.models.task import Task


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve user record directly from database by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve user record directly from database by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
    """Retrieve project record directly from database by ID."""
    return db.query(Project).filter(Project.id == project_id).first()


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """Retrieve task record directly from database by ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def count_projects(db: Session) -> int:
    """Return total count of projects in database."""
    return db.query(Project).count()


def count_tasks(db: Session) -> int:
    """Return total count of tasks in database."""
    return db.query(Task).count()
