# TaskFlow API - Manual API Test Plan

## 1. Objective

The objective of this Test Plan is to outline the testing strategy, scope, environment, tools, and test scenarios for validating the **TaskFlow REST API**. This plan ensures that the backend application provides robust, secure, and reliable API endpoints compliant with functional specifications, validation rules, role-based access controls, and performance sanity bounds.

---

## 2. Scope

### In Scope

- **Authentication Module**: User registration, login authentication, JWT token generation, and current user profile retrieval.
- **Projects Module**: Full CRUD operations on projects (`GET`, `POST`, `PUT`, `DELETE`), project ownership verification, status state transitions.
- **Tasks Module**: Task creation, retrieval, updates, deletion, task status/priority filtering, project/assignee filtering, and page-based pagination.
- **Users Module (Admin Only)**: User listing and individual user lookup protected by Role-Based Access Control (RBAC).
- **Dashboard Module**: Statistical metric aggregation (total projects, total tasks, completed, pending, and high-priority tasks).
- **Database Integrity**: Validation of persistence, foreign key cascading, and table relationships in SQLite/MySQL.

### Out of Scope

- Frontend UI / Mobile client testing.
- High-volume Load & Stress testing (beyond basic response time sanity checks).
- Security penetration testing (e.g., SQL injection, XSS payload testing outside API validation).

---

## 3. API Modules Under Test

| Module Name | Endpoints Covered | Access Level |
| :--- | :--- | :--- |
| **Authentication** | `/api/auth/register`, `/api/auth/login`, `/api/auth/me` | Public / Authenticated |
| **Projects** | `/api/projects`, `/api/projects/{id}` | Authenticated (Owner / Admin) |
| **Tasks** | `/api/tasks`, `/api/tasks/{id}` | Authenticated (Owner / Assignee / Admin) |
| **Users** | `/api/users`, `/api/users/{id}` | Admin Only |
| **Dashboard** | `/api/dashboard` | Authenticated |

---

## 4. Testing Types & Methodologies

1. **Functional Testing**: Validating endpoint responses against business requirements.
2. **Positive Testing**: Verifying successful HTTP status codes (`200 OK`, `201 Created`, `204 No Content`) with valid payloads.
3. **Negative Testing**: Injecting invalid inputs, missing fields, malformed JSON, and verifying error handling (`400 Bad Request`, `422 Unprocessable Entity`).
4. **Boundary Testing**: Testing field length limits, min/max pagination parameters (`page=1`, `limit=100`), edge integer values.
5. **Authentication Testing**: Validating JWT Bearer token lifecycle, expiration, missing headers (`401 Unauthorized`).
6. **Authorization Testing (RBAC)**: Validating normal users cannot access admin endpoints (`403 Forbidden`) or modify other users' projects.
7. **Validation & Contract Testing**: Validating JSON response schema, required keys, data types, and headers.
8. **Error Handling Verification**: Verifying consistent, informative error response format (`{"detail": "..."}`).
9. **Regression Testing**: Re-running automated Pytest suite on code changes.
10. **Database Validation**: Direct database query validation via SQLAlchemy / DB browser to confirm data persistence and clean tear-downs.

---

## 5. Test Environment & Tools

- **Target Application**: TaskFlow REST API (FastAPI + SQLAlchemy + SQLite/MySQL)
- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Documentation**: `http://127.0.0.1:8000/docs` (Swagger UI), `http://127.0.0.1:8000/redoc`
- **Manual Testing Tools**: Postman v10+, Swagger UI, DB Browser for SQLite / DBeaver
- **Automation Tools**: Python 3.11, Requests, Pytest, Pytest-HTML, SQLAlchemy, openpyxl

---

## 6. Entry & Exit Criteria

### Entry Criteria

- TaskFlow API application is fully runnable locally on `http://127.0.0.1:8000`.
- Database seeded with default Admin (`admin@example.com`) and QA User (`qauser@example.com`).
- Interactive Swagger UI documentation is accessible.

### Exit Criteria

- 100% of planned 50+ manual test cases executed and documented.
- 100% of 40+ automated Pytest tests executing with 0 failures.
- HTML Test Report generated and archived in `reports/`.
- All critical and high severity API bugs logged in `API_Bug_Reports.md`.

---

## 7. Risks & Mitigation Strategies

| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **Database State Contamination** | Tests fail due to pre-existing dirty data | Use Pytest fixtures with auto-teardown and DB re-seeding scripts |
| **Port Conflicts (8000)** | Server fails to launch | Support environment variable `PORT` overrides and process cleanup |
| **Token Expiration during test runs** | Authentication failures | Long-lived JWT tokens configured for test environment (24h) |
