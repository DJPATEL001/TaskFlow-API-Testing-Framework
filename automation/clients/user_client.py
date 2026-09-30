from typing import Optional, Dict
import requests
from automation.clients.base_client import BaseClient


class UserClient(BaseClient):
    """API Client for Admin User endpoints."""

    def get_users(self, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get("/api/users", headers=headers)

    def get_user_by_id(self, user_id: int, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get(f"/api/users/{user_id}", headers=headers)
