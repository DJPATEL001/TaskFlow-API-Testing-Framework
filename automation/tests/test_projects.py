import pytest
from automation.clients.project_client import ProjectClient
from automation.config.config import config
from automation.schemas.project_schema import PROJECT_SCHEMA, PROJECT_LIST_SCHEMA
from automation.utils.api_helpers import generate_random_string
from automation.utils.assertions import (
    assert_status_code,
    assert_response_time,
    assert_json_schema,
    assert_response_keys,
    assert_error_message,
)
from automation.utils.db_helpers import get_project_by_id, count_projects


@pytest.mark.projects
class TestProjects:

    def test_create_project_success(self, project_api_client, db_session):
        """TC_PROJ_01: Verify project creation with valid details."""
        proj_name = f"Project {generate_random_string(6)}"
        payload = {
            "name": proj_name,
            "description": "Automated test project description",
            "status": "active",
        }
        response = project_api_client.create_project(payload)
        assert_status_code(response, 201)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, PROJECT_SCHEMA)
        assert data["name"] == proj_name
        assert data["status"] == "active"

        # Database direct verification
        db_proj = get_project_by_id(db_session, data["id"])
        assert db_proj is not None
        assert db_proj.name == proj_name

        # Teardown
        project_api_client.delete_project(data["id"])

    def test_get_projects_list(self, project_api_client):
        """TC_PROJ_02: Verify retrieving user's project list returns 200 OK."""
        response = project_api_client.get_projects()
        assert_status_code(response, 200)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, PROJECT_LIST_SCHEMA)
        assert isinstance(data, list)

    def test_get_project_by_id_success(self, project_api_client, created_project):
        """TC_PROJ_03: Verify retrieving project by valid ID returns 200 OK."""
        project_id = created_project["id"]
        response = project_api_client.get_project_by_id(project_id)
        assert_status_code(response, 200)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, PROJECT_SCHEMA)
        assert data["id"] == project_id
        assert data["name"] == created_project["name"]

    def test_update_project_success(self, project_api_client, created_project, db_session):
        """TC_PROJ_04: Verify updating project details succeeds."""
        project_id = created_project["id"]
        updated_name = f"Updated {generate_random_string(6)}"
        payload = {
            "name": updated_name,
            "description": "Updated project description",
            "status": "completed",
        }
        response = project_api_client.update_project(project_id, payload)
        assert_status_code(response, 200)

        data = response.json()
        assert data["name"] == updated_name
        assert data["status"] == "completed"

        # DB verification
        db_proj = get_project_by_id(db_session, project_id)
        assert db_proj.name == updated_name
        assert db_proj.status == "completed"

    def test_delete_project_success(self, project_api_client, db_session):
        """TC_PROJ_05: Verify deleting project returns 204 No Content and removes record from DB."""
        # Create a temp project specifically to delete
        create_res = project_api_client.create_project({"name": "Temp Project to Delete", "status": "active"})
        assert_status_code(create_res, 201)
        project_id = create_res.json()["id"]

        # Delete project
        del_res = project_api_client.delete_project(project_id)
        assert_status_code(del_res, 204)

        # Direct DB verification: should be None
        db_proj = get_project_by_id(db_session, project_id)
        assert db_proj is None

        # API check: should return 404
        get_res = project_api_client.get_project_by_id(project_id)
        assert_status_code(get_res, 404)

    def test_get_project_invalid_id(self, project_api_client):
        """TC_PROJ_06: Verify retrieving project with non-existent ID returns 404 Not Found."""
        response = project_api_client.get_project_by_id(999999)
        assert_status_code(response, 404)
        assert_error_message(response, "not found")

    def test_create_project_missing_name(self, project_api_client):
        """TC_PROJ_07: Verify project creation without name returns 422 Unprocessable Entity."""
        payload = {"description": "Project with no name"}
        response = project_api_client.create_project(payload)
        assert_status_code(response, 422)

    def test_create_project_invalid_status(self, project_api_client):
        """TC_PROJ_08: Verify project creation with invalid status enum returns 422."""
        payload = {"name": "Test Project", "status": "unknown_status"}
        response = project_api_client.create_project(payload)
        assert_status_code(response, 422)

    def test_projects_unauthorized_access(self, unauthenticated_client):
        """TC_PROJ_09: Verify project endpoints return 401 when accessed without token."""
        client = ProjectClient(base_url=config.BASE_URL)
        response = client.get_projects()
        assert_status_code(response, 401)
