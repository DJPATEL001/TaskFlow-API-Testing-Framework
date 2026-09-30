from typing import Optional, Dict, Any
import requests
from automation.clients.base_client import BaseClient


class TaskClient(BaseClient):
    """API Client for Task endpoints."""

    def get_tasks(self, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get("/api/tasks", params=params, headers=headers)

    def create_task(self, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.post("/api/tasks", json=payload, headers=headers)

    def get_task_by_id(self, task_id: Any, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"/api/tasks/{task_id}", headers=headers)

    def update_task(self, task_id: Any, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.put(f"/api/tasks/{task_id}", json=payload, headers=headers)

    def delete_task(self, task_id: Any, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.delete(f"/api/tasks/{task_id}", headers=headers)
