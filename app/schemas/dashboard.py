from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_projects: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    high_priority_tasks: int
