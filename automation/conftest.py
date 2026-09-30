import pytest
from app.database import SessionLocal
from automation.config.config import config
from automation.clients.auth_client import AuthClient
from automation.clients.project_client import ProjectClient
from automation.clients.task_client import TaskClient
from automation.clients.user_client import UserClient
from automation.clients.dashboard_client import DashboardClient
from automation.clients.base_client import BaseClient


@pytest.fixture(scope="session")
def base_url():
    """Return base API URL."""
    return config.BASE_URL


@pytest.fixture(scope="session")
def unauthenticated_client():
    """Return an API client without authentication token."""
    return BaseClient(base_url=config.BASE_URL)


@pytest.fixture(scope="session")
def auth_token():
    """Authenticate QA user and return JWT access token."""
    client = AuthClient(base_url=config.BASE_URL)
    response = client.login(config.TEST_USER_EMAIL, config.TEST_USER_PASSWORD)
    assert response.status_code == 200, f"QA User login failed: {response.text}"
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def admin_auth_token():
    """Authenticate System Admin user and return JWT access token."""
    client = AuthClient(base_url=config.BASE_URL)
    response = client.login(config.ADMIN_EMAIL, config.ADMIN_PASSWORD)
    assert response.status_code == 200, f"Admin login failed: {response.text}"
    return response.json()["access_token"]


@pytest.fixture
def authenticated_client(auth_token):
    """Return BaseClient initialized with QA User Bearer token."""
    return BaseClient(base_url=config.BASE_URL, token=auth_token)


@pytest.fixture
def admin_client(admin_auth_token):
    """Return BaseClient initialized with Admin Bearer token."""
    return BaseClient(base_url=config.BASE_URL, token=admin_auth_token)


@pytest.fixture
def auth_api_client():
    """Return AuthClient instance."""
    return AuthClient(base_url=config.BASE_URL)


@pytest.fixture
def project_api_client(auth_token):
    """Return ProjectClient initialized with QA User token."""
    return ProjectClient(base_url=config.BASE_URL, token=auth_token)


@pytest.fixture
def task_api_client(auth_token):
    """Return TaskClient initialized with QA User token."""
    return TaskClient(base_url=config.BASE_URL, token=auth_token)


@pytest.fixture
def user_api_client(admin_auth_token):
    """Return UserClient initialized with Admin token."""
    return UserClient(base_url=config.BASE_URL, token=admin_auth_token)


@pytest.fixture
def dashboard_api_client(auth_token):
    """Return DashboardClient initialized with QA User token."""
    return DashboardClient(base_url=config.BASE_URL, token=auth_token)


@pytest.fixture
def created_project(project_api_client):
    """Fixture to create a test project and automatically clean it up after test execution."""
    payload = {
        "name": "Fixture Temporary Project",
        "description": "Created for fixture testing and tear-down validation",
        "status": "active",
    }
    response = project_api_client.create_project(payload)
    assert response.status_code == 201, f"Fixture project creation failed: {response.text}"
    project_data = response.json()
    yield project_data

    # Cleanup teardown
    cleanup_res = project_api_client.delete_project(project_data["id"])
    assert cleanup_res.status_code in [204, 404]


@pytest.fixture
def created_task(task_api_client, created_project):
    """Fixture to create a test task associated with created_project and tear down after test."""
    payload = {
        "title": "Fixture Temporary Task",
        "description": "Created for fixture testing and tear-down validation",
        "priority": "high",
        "status": "todo",
        "project_id": created_project["id"],
    }
    response = task_api_client.create_task(payload)
    assert response.status_code == 201, f"Fixture task creation failed: {response.text}"
    task_data = response.json()
    yield task_data

    # Cleanup teardown
    cleanup_res = task_api_client.delete_task(task_data["id"])
    assert cleanup_res.status_code in [204, 404]


@pytest.fixture
def db_session():
    """SQLAlchemy database session fixture for direct database validation in tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
