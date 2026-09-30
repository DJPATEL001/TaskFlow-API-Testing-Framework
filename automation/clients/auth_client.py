from typing import Optional, Dict, Any
import requests
from automation.clients.base_client import BaseClient


class AuthClient(BaseClient):
    """API Client for Authentication endpoints."""

    def register(self, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.post("/api/auth/register", json=payload, headers=headers)

    def login(self, email: str, password: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        payload = {"email": email, "password": password}
        return self.post("/api/auth/login", json=payload, headers=headers)

    def get_me(self, token: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        req_headers = headers or {}
        if token:
            req_headers["Authorization"] = f"Bearer {token}"
        return self.get("/api/auth/me", headers=req_headers)
