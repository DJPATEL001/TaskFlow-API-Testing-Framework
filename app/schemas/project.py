from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


ProjectStatus = Literal["active", "completed", "archived"]


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, example="Automation Framework")
    description: Optional[str] = Field(None, example="API Automation Framework development")
    status: ProjectStatus = Field("active", example="active")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150, example="Updated Project Name")
    description: Optional[str] = Field(None, example="Updated description")
    status: Optional[ProjectStatus] = Field(None, example="completed")


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
