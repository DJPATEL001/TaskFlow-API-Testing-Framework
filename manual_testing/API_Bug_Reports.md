# TaskFlow API - Manual Bug Reports

This document contains 5 detailed, realistic API bug reports identified during manual and exploratory testing of the **TaskFlow REST API**.

---

## Bug Report 1: User Registration Allows White Space Password

- **Bug ID**: BUG-API-001
- **Title**: User registration endpoint accepts passwords containing leading/trailing whitespaces without stripping or validation
- **Endpoint**: `/api/auth/register`
- **HTTP Method**: `POST`
- **Environment**: Local Staging Environment (v1.0.0, Python 3.11, FastAPI, SQLite)
- **Preconditions**: API Server is active and accessible.
- **Steps to Reproduce**:
  1. Open Postman or curl.
  2. Send a `POST` request to `http://127.0.0.1:8000/api/auth/register`.
  3. Include JSON body with password containing only spaces: `"   "` (3 spaces).
- **Request Body**:
  ```json
  {
    "name": "Whitespace User",
    "email": "spacepass@example.com",
    "password": "   "
  }
  ```
- **Expected Response**: `422 Unprocessable Entity` or `400 Bad Request` indicating password cannot be empty or consist solely of whitespace characters.
- **Actual Response**: `201 Created` returning user object with hashed whitespace password.
- **Expected Status Code**: `400 Bad Request` / `422 Unprocessable Entity`
- **Actual Status Code**: `201 Created`
- **Severity**: High
- **Priority**: High
- **Status**: Open
- **Notes / Impact**: Allows creation of insecure accounts that are susceptible to accidental login failures or authentication lockouts.

---

## Bug Report 2: Normal User Can Delete Tasks Assigned to Other Users

- **Bug ID**: BUG-API-002
- **Title**: Missing ownership and assignment verification on `DELETE /api/tasks/{id}` endpoint allows unauthorized task deletion
- **Endpoint**: `/api/tasks/{id}`
- **HTTP Method**: `DELETE`
- **Environment**: Local Staging Environment (v1.0.0, FastAPI)
- **Preconditions**:
  1. User A owns Project 1 and Task 10.
  2. User B logs in and obtains a valid JWT token.
- **Steps to Reproduce**:
  1. Authenticate as User B.
  2. Send `DELETE` request to `http://127.0.0.1:8000/api/tasks/10` with User B's Bearer token.
- **Request Headers**:
  ```http
  Authorization: Bearer <User_B_Token>
  ```
- **Expected Response**: `403 Forbidden` with detail `"Access forbidden: You do not own or control this task"`.
- **Actual Response**: `204 No Content` and Task 10 is permanently deleted from SQLite DB.
- **Expected Status Code**: `403 Forbidden`
- **Actual Status Code**: `204 No Content`
- **Severity**: High
- **Priority**: High
- **Status**: Open
- **Notes / Impact**: Security flaw allowing cross-user data destruction across projects.

---

## Bug Report 3: Task Pagination Accepts Negative `limit` and `page` Values

- **Bug ID**: BUG-API-003
- **Title**: Query parameter pagination does not reject negative integers for `page` or `limit`
- **Endpoint**: `/api/tasks`
- **HTTP Method**: `GET`
- **Environment**: Local Staging Environment (v1.0.0)
- **Preconditions**: Authenticated user.
- **Steps to Reproduce**:
  1. Send `GET` request to `/api/tasks?page=-1&limit=-10`.
- **Request URL**:
  ```http
  GET /api/tasks?page=-1&limit=-10
  Authorization: Bearer <valid_token>
  ```
- **Expected Response**: `422 Unprocessable Entity` with query parameter validation error indicating `page` and `limit` must be greater than or equal to 1 (`ge=1`).
- **Actual Response**: `200 OK` with negative offset resulting in unexpected full list or internal offset miscalculation.
- **Expected Status Code**: `422 Unprocessable Entity`
- **Actual Status Code**: `200 OK`
- **Severity**: Medium
- **Priority**: Medium
- **Status**: Open
- **Notes / Impact**: Causes pagination calculation anomalies and potential database query errors on certain SQL dialects.

---

## Bug Report 4: Incorrect Total Count in Task Filtering by Invalid Priority

- **Bug ID**: BUG-API-004
- **Title**: `GET /api/tasks?priority=nonexistent` returns 200 OK with `pages: 1` instead of `pages: 0` when zero items match
- **Endpoint**: `/api/tasks`
- **HTTP Method**: `GET`
- **Environment**: Local Staging Environment (v1.0.0)
- **Preconditions**: Authenticated user.
- **Steps to Reproduce**:
  1. Send `GET` request to `/api/tasks?priority=low` when no tasks have low priority in the database.
- **Request URL**:
  ```http
  GET /api/tasks?priority=low
  ```
- **Expected Response**:
  ```json
  {
    "items": [],
    "total": 0,
    "page": 1,
    "limit": 10,
    "pages": 0
  }
  ```
- **Actual Response**:
  ```json
  {
    "items": [],
    "total": 0,
    "page": 1,
    "limit": 10,
    "pages": 1
  }
  ```
- **Expected Status Code**: `200 OK`
- **Actual Status Code**: `200 OK`
- **Severity**: Low
- **Priority**: Medium
- **Status**: Open
- **Notes / Impact**: Frontend UI components relying on `pages` metric display page 1 pagination controls when no records exist.

---

## Bug Report 5: User Profile Update Exposes Internal SQL Foreign Key Error on Invalid Assignee

- **Bug ID**: BUG-API-005
- **Title**: Task update endpoint with non-existent `assigned_to` returns 400 Bad Request but leaks detailed raw exception instead of structured message
- **Endpoint**: `/api/tasks/{id}`
- **HTTP Method**: `PUT`
- **Environment**: Local Staging Environment (v1.0.0)
- **Preconditions**: Task 1 exists in DB.
- **Steps to Reproduce**:
  1. Send `PUT` request to `/api/tasks/1` with payload `{"assigned_to": 999999}`.
- **Request Body**:
  ```json
  {
    "assigned_to": 999999
  }
  ```
- **Expected Response**:
  ```json
  {
    "detail": "Assigned user with ID 999999 does not exist"
  }
  ```
- **Actual Response**:
  ```json
  {
    "detail": "Assigned user with ID 999999 does not exist"
  }
  ```
  *(Note: In previous build v0.9, raw SQLAlchemy IntegrityError was exposed. Verified fix in current build).*
- **Expected Status Code**: `400 Bad Request`
- **Actual Status Code**: `400 Bad Request`
- **Severity**: Medium
- **Priority**: Low
- **Status**: Closed (Verified Fixed)
