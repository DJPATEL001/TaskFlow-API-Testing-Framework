import requests
from typing import Optional, Dict, Any
from automation.config.config import config


class BaseClient:
    """Base API client wrapping requests.Session with timing and custom headers handling."""

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        self.base_url = (base_url or config.BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        if token:
            self.set_token(token)

    def set_token(self, token: str):
        """Set Bearer token for authenticated requests."""
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        """Remove Authorization header."""
        self.session.headers.pop("Authorization", None)

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
        )
        return response

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint: str, json: Optional[Any] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("POST", endpoint, json=json, headers=headers)

    def put(self, endpoint: str, json: Optional[Any] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("PUT", endpoint, json=json, headers=headers)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.request("DELETE", endpoint, headers=headers)
