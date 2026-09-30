import pytest
from automation.clients.task_client import TaskClient
from automation.config.config import config
from automation.schemas.task_schema import TASK_SCHEMA, TASK_LIST_RESPONSE_SCHEMA
from automation.utils.api_helpers import generate_random_string
from automation.utils.assertions import (
    assert_status_code,
    assert_response_time,
    assert_json_schema,
    assert_response_keys,
    assert_error_message,
)
from automation.utils.db_helpers import get_task_by_id, count_tasks


@pytest.mark.tasks
class TestTasks:

    def test_create_task_success(self, task_api_client, created_project, db_session):
        """TC_TASK_01: Verify task creation under valid project."""
        task_title = f"Task {generate_random_string(6)}"
        payload = {
            "title": task_title,
            "description": "Automated task description",
            "priority": "high",
            "status": "todo",
            "project_id": created_project["id"],
        }
        response = task_api_client.create_task(payload)
        assert_status_code(response, 201)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, TASK_SCHEMA)
        assert data["title"] == task_title
        assert data["priority"] == "high"
        assert data["project_id"] == created_project["id"]

        # Direct DB verification
        db_task = get_task_by_id(db_session, data["id"])
        assert db_task is not None
        assert db_task.title == task_title

        # Teardown
        task_api_client.delete_task(data["id"])

    def test_get_tasks_list(self, task_api_client):
        """TC_TASK_02: Verify retrieving tasks list returns paginated TaskListResponse."""
        response = task_api_client.get_tasks()
        assert_status_code(response, 200)
        assert_response_time(response)

        data = response.json()
        assert_json_schema(data, TASK_LIST_RESPONSE_SCHEMA)
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data

    def test_get_task_by_id_success(self, task_api_client, created_task):
        """TC_TASK_03: Verify retrieving task by valid ID returns 200 OK."""
        task_id = created_task["id"]
        response = task_api_client.get_task_by_id(task_id)
        assert_status_code(response, 200)

        data = response.json()
        assert_json_schema(data, TASK_SCHEMA)
        assert data["id"] == task_id
        assert data["title"] == created_task["title"]

    def test_update_task_success(self, task_api_client, created_task, db_session):
        """TC_TASK_04: Verify updating task priority, status, and title."""
        task_id = created_task["id"]
        updated_title = f"Updated Task {generate_random_string(4)}"
        payload = {
            "title": updated_title,
            "priority": "critical",
            "status": "in_progress",
        }
        response = task_api_client.update_task(task_id, payload)
        assert_status_code(response, 200)

        data = response.json()
        assert data["title"] == updated_title
        assert data["priority"] == "critical"
        assert data["status"] == "in_progress"

        # DB verification
        db_task = get_task_by_id(db_session, task_id)
        assert db_task.title == updated_title
        assert db_task.priority == "critical"

    def test_delete_task_success(self, task_api_client, created_project, db_session):
        """TC_TASK_05: Verify deleting task returns 204 No Content and removes from DB."""
        # Create temp task
        payload = {"title": "Temp Task", "project_id": created_project["id"]}
        create_res = task_api_client.create_task(payload)
        assert_status_code(create_res, 201)
        task_id = create_res.json()["id"]

        # Delete task
        del_res = task_api_client.delete_task(task_id)
        assert_status_code(del_res, 204)

        # DB check
        assert get_task_by_id(db_session, task_id) is None

    def test_filter_tasks_by_status(self, task_api_client):
        """TC_TASK_06: Verify filtering tasks by status=completed."""
        response = task_api_client.get_tasks(params={"status": "completed"})
        assert_status_code(response, 200)

        data = response.json()
        for item in data["items"]:
            assert item["status"] == "completed"

    def test_filter_tasks_by_priority(self, task_api_client):
        """TC_TASK_07: Verify filtering tasks by priority=high."""
        response = task_api_client.get_tasks(params={"priority": "high"})
        assert_status_code(response, 200)

        data = response.json()
        for item in data["items"]:
            assert item["priority"] == "high"

    def test_filter_tasks_by_project_id(self, task_api_client, created_project, created_task):
        """TC_TASK_08: Verify filtering tasks by project_id."""
        project_id = created_project["id"]
        response = task_api_client.get_tasks(params={"project_id": project_id})
        assert_status_code(response, 200)

        data = response.json()
        assert len(data["items"]) >= 1
        for item in data["items"]:
            assert item["project_id"] == project_id

    def test_tasks_pagination(self, task_api_client):
        """TC_TASK_09: Verify task list pagination page and limit parameters."""
        response = task_api_client.get_tasks(params={"page": 1, "limit": 2})
        assert_status_code(response, 200)

        data = response.json()
        assert data["page"] == 1
        assert data["limit"] == 2
        assert len(data["items"]) <= 2

    def test_get_task_invalid_id(self, task_api_client):
        """TC_TASK_10: Verify retrieving non-existent task ID returns 404 Not Found."""
        response = task_api_client.get_task_by_id(999999)
        assert_status_code(response, 404)
        assert_error_message(response, "not found")

    def test_create_task_missing_title(self, task_api_client, created_project):
        """TC_TASK_11: Verify task creation without required title returns 422."""
        payload = {"project_id": created_project["id"]}
        response = task_api_client.create_task(payload)
        assert_status_code(response, 422)

    def test_create_task_invalid_priority_enum(self, task_api_client, created_project):
        """TC_TASK_12: Verify task creation with invalid priority enum returns 422."""
        payload = {
            "title": "Invalid Priority Task",
            "priority": "super_high",
            "project_id": created_project["id"],
        }
        response = task_api_client.create_task(payload)
        assert_status_code(response, 422)

    def test_create_task_invalid_status_enum(self, task_api_client, created_project):
        """TC_TASK_13: Verify task creation with invalid status enum returns 422."""
        payload = {
            "title": "Invalid Status Task",
            "status": "pending_review",
            "project_id": created_project["id"],
        }
        response = task_api_client.create_task(payload)
        assert_status_code(response, 422)

    def test_create_task_nonexistent_project_id(self, task_api_client):
        """TC_TASK_14: Verify task creation with non-existent project_id returns 400 Bad Request."""
        payload = {
            "title": "Orphan Task",
            "project_id": 999999,
        }
        response = task_api_client.create_task(payload)
        assert_status_code(response, 400)
        assert_error_message(response, "does not exist")
