from typing import Optional, Dict, Any
import requests
from automation.clients.base_client import BaseClient


class ProjectClient(BaseClient):
    """API Client for Project endpoints."""

    def get_projects(self, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get("/api/projects", headers=headers)

    def create_project(self, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.post("/api/projects", json=payload, headers=headers)

    def get_project_by_id(self, project_id: Any, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"/api/projects/{project_id}", headers=headers)

    def update_project(self, project_id: Any, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.put(f"/api/projects/{project_id}", json=payload, headers=headers)

    def delete_project(self, project_id: Any, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.delete(f"/api/projects/{project_id}", headers=headers)
