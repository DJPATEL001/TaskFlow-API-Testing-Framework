from typing import Optional, Dict
import requests
from automation.clients.base_client import BaseClient


class DashboardClient(BaseClient):
    """API Client for Dashboard endpoints."""

    def get_dashboard(self, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.get("/api/dashboard", headers=headers)
