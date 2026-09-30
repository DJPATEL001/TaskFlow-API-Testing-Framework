from typing import Any, List, Dict
import requests
from jsonschema import validate, ValidationError


def assert_status_code(response: requests.Response, expected_code: int):
    """Assert HTTP response status code with detailed failure output."""
    assert response.status_code == expected_code, (
        f"Expected HTTP status code {expected_code}, but got {response.status_code}. "
        f"Response body: {response.text}"
    )


def assert_response_time(response: requests.Response, max_seconds: float = 2.0):
    """Sanity check assertion on basic response time."""
    elapsed = response.elapsed.total_seconds()
    assert elapsed < max_seconds, (
        f"Response time exceeded target! Expected < {max_seconds}s, actual: {elapsed:.3f}s"
    )


def assert_json_schema(data: Any, schema: Dict[str, Any]):
    """Validate JSON data structure against standard JSON Schema."""
    try:
        validate(instance=data, schema=schema)
    except ValidationError as err:
        raise AssertionError(f"JSON Schema validation failed: {err.message}")


def assert_response_keys(response_json: dict, expected_keys: List[str]):
    """Assert that all expected keys exist in the response dictionary."""
    for key in expected_keys:
        assert key in response_json, f"Key '{key}' missing from API response dictionary: {response_json}"


def assert_error_message(response: requests.Response, expected_substring: str):
    """Assert that error response contains expected detail message."""
    data = response.json()
    detail = data.get("detail", "")
    if isinstance(detail, list):
        # FastAPI validation errors list of dicts
        found = any(expected_substring.lower() in str(item).lower() for item in detail)
        assert found, f"Expected substring '{expected_substring}' in validation errors: {detail}"
    else:
        assert expected_substring.lower() in str(detail).lower(), (
            f"Expected error detail containing '{expected_substring}', but got '{detail}'"
        )
