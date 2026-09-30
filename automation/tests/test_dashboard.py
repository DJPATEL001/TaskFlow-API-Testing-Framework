import pytest
from automation.clients.dashboard_client import DashboardClient
from automation.config.config import config
from automation.schemas.dashboard_schema import DASHBOARD_SCHEMA
from automation.utils.assertions import (
    assert_status_code,
    assert_response_time,
    assert_json_schema,
    assert_error_message,
)
from automation.utils.db_helpers import count_projects, count_tasks
from app.models.task import Task


@pytest.mark.dashboard
class TestDashboard:

    def test_get_dashboard_authenticated(self, dashboard_api_client):
        """TC_DASH_01: Verify authenticated dashboard returns 200 OK with correct JSON schema."""
        response = dashboard_api_client.get_dashboard()
        assert_status_code(response, 200)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, DASHBOARD_SCHEMA)

    def test_dashboard_statistics_match_database(self, dashboard_api_client, db_session):
        """TC_DASH_02: Verify dashboard metrics accurately reflect database record counts."""
        response = dashboard_api_client.get_dashboard()
        assert_status_code(response, 200)

        data = response.json()

        # Database direct counts
        expected_total_projects = count_projects(db_session)
        expected_total_tasks = count_tasks(db_session)
        expected_completed = db_session.query(Task).filter(Task.status == "completed").count()
        expected_pending = db_session.query(Task).filter(Task.status.in_(["todo", "in_progress"])).count()
        expected_high_priority = db_session.query(Task).filter(Task.priority.in_(["high", "critical"])).count()

        assert data["total_projects"] == expected_total_projects
        assert data["total_tasks"] == expected_total_tasks
        assert data["completed_tasks"] == expected_completed
        assert data["pending_tasks"] == expected_pending
        assert data["high_priority_tasks"] == expected_high_priority

    def test_dashboard_unauthorized_access(self, unauthenticated_client):
        """TC_DASH_03: Verify unauthenticated request to dashboard returns 401 Unauthorized."""
        client = DashboardClient(base_url=config.BASE_URL)
        response = client.get_dashboard()
        assert_status_code(response, 401)
        assert_error_message(response, "missing")

    def test_dashboard_invalid_token(self, unauthenticated_client):
        """TC_DASH_04: Verify invalid token request to dashboard returns 401 Unauthorized."""
        client = DashboardClient(base_url=config.BASE_URL, token="invalid_token_xyz")
        response = client.get_dashboard()
        assert_status_code(response, 401)
        assert_error_message(response, "Invalid")
