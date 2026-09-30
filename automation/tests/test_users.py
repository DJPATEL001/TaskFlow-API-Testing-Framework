import pytest
from automation.clients.user_client import UserClient
from automation.config.config import config
from automation.schemas.auth_schema import USER_SCHEMA
from automation.utils.assertions import (
    assert_status_code,
    assert_response_time,
    assert_json_schema,
    assert_error_message,
)


@pytest.mark.users
class TestUsers:

    def test_admin_get_users(self, user_api_client):
        """TC_USER_01: Verify admin user can retrieve all users."""
        response = user_api_client.get_users()
        assert_status_code(response, 200)
        assert_response_time(response)

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # Admin + QA user

    def test_admin_get_user_by_id(self, user_api_client):
        """TC_USER_02: Verify admin user can retrieve a user by ID."""
        response = user_api_client.get_user_by_id(1)
        assert_status_code(response, 200)

        data = response.json()
        assert_json_schema(data, USER_SCHEMA)
        assert data["id"] == 1

    def test_admin_get_nonexistent_user(self, user_api_client):
        """TC_USER_03: Verify admin receiving 404 Not Found for non-existent user ID."""
        response = user_api_client.get_user_by_id(999999)
        assert_status_code(response, 404)
        assert_error_message(response, "not found")

    def test_normal_user_cannot_access_users(self, authenticated_client):
        """TC_USER_04: Verify normal non-admin user receives 403 Forbidden accessing /api/users."""
        client = UserClient(base_url=config.BASE_URL, token=authenticated_client.session.headers["Authorization"].split()[1])
        response = client.get_users()
        assert_status_code(response, 403)
        assert_error_message(response, "Admin privilege required")

    def test_normal_user_cannot_access_user_by_id(self, authenticated_client):
        """TC_USER_05: Verify normal non-admin user receives 403 Forbidden accessing /api/users/{id}."""
        client = UserClient(base_url=config.BASE_URL, token=authenticated_client.session.headers["Authorization"].split()[1])
        response = client.get_user_by_id(1)
        assert_status_code(response, 403)
        assert_error_message(response, "Admin privilege required")

    def test_users_unauthorized_access(self, unauthenticated_client):
        """TC_USER_06: Verify unauthenticated request to /api/users returns 401 Unauthorized."""
        client = UserClient(base_url=config.BASE_URL)
        response = client.get_users()
        assert_status_code(response, 401)
