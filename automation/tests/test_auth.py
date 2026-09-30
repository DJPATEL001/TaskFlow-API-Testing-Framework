import pytest
from automation.clients.auth_client import AuthClient
from automation.schemas.auth_schema import LOGIN_RESPONSE_SCHEMA, USER_SCHEMA
from automation.utils.api_helpers import generate_random_email, load_test_data
from automation.utils.assertions import (
    assert_status_code,
    assert_response_time,
    assert_json_schema,
    assert_response_keys,
    assert_error_message,
)
from automation.utils.db_helpers import get_user_by_email


@pytest.mark.auth
class TestAuth:

    def test_register_valid_user(self, auth_api_client, db_session):
        """TC_AUTH_01: Verify user registration with valid details."""
        email = generate_random_email("reg_test")
        payload = {
            "name": "Automation Tester",
            "email": email,
            "password": "TestPassword@123",
        }
        response = auth_api_client.register(payload)
        assert_status_code(response, 201)
        assert_response_time(response)

        data = response.json()
        assert_response_keys(data, ["id", "name", "email", "role", "created_at"])
        assert "password" not in data
        assert "password_hash" not in data
        assert data["email"] == email
        assert data["name"] == "Automation Tester"
        assert data["role"] == "user"

        # DB Validation
        db_user = get_user_by_email(db_session, email)
        assert db_user is not None
        assert db_user.name == "Automation Tester"

    def test_register_duplicate_email(self, auth_api_client):
        """TC_AUTH_02: Verify duplicate user registration fails with 400 Bad Request."""
        email = generate_random_email("dup_test")
        payload = {"name": "First User", "email": email, "password": "Test@12345"}
        res1 = auth_api_client.register(payload)
        assert_status_code(res1, 201)

        # Attempt duplicate registration
        res2 = auth_api_client.register(payload)
        assert_status_code(res2, 400)
        assert_error_message(res2, "already registered")

    def test_register_invalid_email_format(self, auth_api_client):
        """TC_AUTH_03: Verify registration with invalid email format returns 422."""
        payload = {
            "name": "Invalid Email User",
            "email": "not-an-email-address",
            "password": "Test@12345",
        }
        response = auth_api_client.register(payload)
        assert_status_code(response, 422)

    def test_register_missing_name(self, auth_api_client):
        """TC_AUTH_04: Verify registration missing required field 'name' returns 422."""
        payload = {
            "email": generate_random_email("missing_name"),
            "password": "Test@12345",
        }
        response = auth_api_client.register(payload)
        assert_status_code(response, 422)

    def test_register_missing_password(self, auth_api_client):
        """TC_AUTH_05: Verify registration missing required field 'password' returns 422."""
        payload = {
            "name": "No Password User",
            "email": generate_random_email("missing_pass"),
        }
        response = auth_api_client.register(payload)
        assert_status_code(response, 422)

    def test_register_short_password(self, auth_api_client):
        """TC_AUTH_06: Verify registration with password shorter than minimum length returns 422."""
        payload = {
            "name": "Short Pass User",
            "email": generate_random_email("short_pass"),
            "password": "123",
        }
        response = auth_api_client.register(payload)
        assert_status_code(response, 422)

    def test_login_valid_credentials(self, auth_api_client):
        """TC_AUTH_07: Verify valid login returns 200 OK and JWT access token."""
        test_data = load_test_data()
        response = auth_api_client.login(
            email="qauser@example.com",
            password="Test@12345",
        )
        assert_status_code(response, 200)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, LOGIN_RESPONSE_SCHEMA)
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "qauser@example.com"

    def test_login_invalid_password(self, auth_api_client):
        """TC_AUTH_08: Verify login with incorrect password returns 401 Unauthorized."""
        response = auth_api_client.login("qauser@example.com", "WrongPassword999")
        assert_status_code(response, 401)
        assert_error_message(response, "Invalid email or password")

    def test_login_invalid_email(self, auth_api_client):
        """TC_AUTH_09: Verify login with non-existent email returns 401 Unauthorized."""
        response = auth_api_client.login("nonexistent_user@example.com", "Test@12345")
        assert_status_code(response, 401)
        assert_error_message(response, "Invalid email or password")

    def test_get_me_valid_token(self, auth_api_client, auth_token):
        """TC_AUTH_10: Verify GET /api/auth/me returns current user profile for valid token."""
        response = auth_api_client.get_me(token=auth_token)
        assert_status_code(response, 200)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, USER_SCHEMA)
        assert data["email"] == "qauser@example.com"

    def test_get_me_missing_token(self, auth_api_client):
        """TC_AUTH_11: Verify GET /api/auth/me returns 401 Unauthorized when token is missing."""
        response = auth_api_client.get_me()
        assert_status_code(response, 401)
        assert_error_message(response, "missing")

    def test_get_me_invalid_token(self, auth_api_client):
        """TC_AUTH_12: Verify GET /api/auth/me returns 401 Unauthorized for malformed token."""
        response = auth_api_client.get_me(token="invalid.malformed.jwttokenstring")
        assert_status_code(response, 401)
        assert_error_message(response, "Invalid")
