from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserResponse
from app.services.auth_service import get_admin_user

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Admin-only endpoint to retrieve all users."""
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Admin-only endpoint to retrieve a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user
