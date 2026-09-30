from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Test User")
    email: EmailStr = Field(..., example="qauser@example.com")
    password: str = Field(..., min_length=6, example="Test@12345")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="qauser@example.com")
    password: str = Field(..., example="Test@12345")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
