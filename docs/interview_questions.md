# TaskFlow API - Technical Interview Preparation Guide

This document contains comprehensive, technically accurate interview questions and answers designed specifically for a **QA Automation Engineer / SDET Fresher portfolio** based on the **TaskFlow REST API Automation Framework**.

---

## 1. REST API Fundamentals

### Q1: What is an API?
**Answer:** An API (Application Programming Interface) is a computing interface and contract that allows two software components or systems to communicate and exchange data using a defined set of protocols, requests, and formats.

### Q2: What is REST?
**Answer:** REST (Representational State Transfer) is an architectural style for designing networked applications. It relies on a stateless, client-server protocol (almost always HTTP). Key principles of REST include:
- **Statelessness**: Every request contains all necessary information; the server stores no client session context.
- **Resource-based**: System entities are identified as resources via uniform URIs (e.g., `/api/projects`).
- **Standard HTTP Methods**: Operations map to HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
- **Representation**: Data is exchanged in formats such as JSON or XML.

### Q3: How does REST differ from SOAP?
**Answer:**
- **Protocol**: SOAP is a rigid XML protocol with strict WS-Security standards; REST is an architectural style using standard HTTP protocols.
- **Format**: SOAP strictly uses XML; REST primarily uses light JSON, XML, or plain text.
- **Performance**: REST is lighter and faster due to smaller JSON payloads and caching capabilities.

### Q4: What is HTTP and JSON?
**Answer:**
- **HTTP (Hypertext Transfer Protocol)**: The foundation data communication protocol of the Web.
- **JSON (JavaScript Object Notation)**: A lightweight, human-readable text format for storing and transporting structured data using key-value pairs and arrays.

### Q5: What is an Endpoint?
**Answer:** An endpoint is a specific URI (Uniform Resource Identifier) where an API can be accessed to perform operations on resources (e.g., `http://127.0.0.1:8000/api/tasks`).

---

## 2. HTTP Methods & Status Codes

### Q6: Explain the standard HTTP Methods.
- **GET**: Retrieves resource representations without modifying server state (Safe & Idempotent).
- **POST**: Creates a new resource on the server (Non-Idempotent).
- **PUT**: Replaces an existing resource or creates it if non-existent (Idempotent).
- **PATCH**: Partially updates specific attributes of an existing resource.
- **DELETE**: Removes a resource from the server (Idempotent).

### Q7: Explain essential HTTP Status Codes and their usage in TaskFlow API.
- **200 OK**: Request succeeded (e.g., `GET /api/projects`, `PUT /api/tasks/1`).
- **201 Created**: Resource successfully created (e.g., `POST /api/auth/register`, `POST /api/tasks`).
- **204 No Content**: Action succeeded with no body returned (e.g., `DELETE /api/projects/1`).
- **400 Bad Request**: Malformed payload or domain rule violation (e.g., Duplicate email or non-existent FK `project_id`).
- **401 Unauthorized**: Authentication missing, expired, or invalid token.
- **403 Forbidden**: Authenticated user lacks permission for the resource (e.g., Normal user accessing `/api/users`).
- **404 Not Found**: Resource URI or ID does not exist in the database (e.g., `GET /api/tasks/9999`).
- **422 Unprocessable Entity**: Pydantic input validation failure (missing required fields or invalid enum type).
- **500 Internal Server Error**: Unexpected backend exception or server failure.

---

## 3. Authentication & Security (JWT)

### Q8: What is JWT and how does Bearer Token Authentication work?
**Answer:** JWT (JSON Web Token) is a compact, URL-safe format for securely transmitting information as a JSON object signed with a cryptographic secret key (`HS256`).
- **Flow**: User sends credentials via `POST /api/auth/login`. Server verifies credentials and returns a signed `access_token`. Client sends this token in subsequent requests via header:
  ```http
  Authorization: Bearer <access_token>
  ```
- Server decodes token, extracts user identity (`sub`), and grants access without hitting a session store.

### Q9: What is the difference between Authentication and Authorization?
- **Authentication**: Verifying **who** the user is (e.g., checking email/password or JWT token validity).
- **Authorization**: Verifying **what permissions** an authenticated user has (e.g., checking if `user.role == 'admin'` before allowing access to `/api/users`).

---

## 4. API Testing Concepts

### Q10: Why perform API Testing over UI Testing?
- **Speed & Execution Time**: API tests run in seconds without waiting for DOM rendering or browser launch.
- **Early Bug Detection**: Enables Shift-Left testing before UI development is completed.
- **Flakiness Reduction**: API contracts are stable compared to fragile UI locators.
- **Security & Contract Validation**: Directly verifies edge cases, validation rules, and authorization bounds.

### Q11: Explain Positive, Negative, and Boundary Testing in APIs.
- **Positive Testing**: Verifying happy paths with valid headers and payloads (returns 200/201).
- **Negative Testing**: Intentionally providing invalid data, missing headers, or unauthorized tokens to verify robust error handling (returns 400, 401, 403, 422).
- **Boundary Testing**: Testing edge limits (e.g., password lengths, `limit=100`, page boundaries).

---

## 5. Pytest & Automation Architecture

### Q12: Why did you create an API Client Layer (`BaseClient`, `AuthClient`, `TaskClient`)?
**Answer:**
To separate API request execution from test assertion logic. Without a client layer, raw `requests.post()` calls with duplicate headers, URLs, and timing parameters would be duplicated across 45+ test files.
- **Benefits**: DRY principle, central header/token management, unified base URL configuration, easy maintenance if endpoints change.

### Q13: How do Pytest Fixtures and `conftest.py` eliminate duplicate login code?
**Answer:**
In `conftest.py`, session-scoped fixtures `auth_token` and `admin_auth_token` perform login once per test session. Function-scoped fixtures `authenticated_client` and `admin_client` inject pre-configured headers into tests.
- Individual tests accept `authenticated_client` as an argument without ever calling `/api/auth/login` explicitly.

### Q14: How do you verify API changes in the Database?
**Answer:**
Using SQLAlchemy direct DB queries (`db_helpers.py`).
- Example: After executing `POST /api/projects`, test queries `db_session.query(Project).filter(Project.id == res.json()['id']).first()` to confirm exact column values, timestamp updates, and foreign key persistence.

---

## 6. Postman & Reporting

### Q15: How does your Postman collection automatically handle JWT Tokens?
**Answer:**
In the Login request `Tests` tab, a JavaScript script parses the JSON response and stores `access_token` into Postman environment variables:
```javascript
var jsonData = pm.response.json();
pm.environment.set("access_token", jsonData.access_token);
```
Subsequent requests reference `Authorization: Bearer {{access_token}}`.

---

## 7. Project Reflection & Problem Solving

### Q16: Walk me through one automated test from start to finish.
**Answer:**
Let's take `test_create_task_success`:
1. **Fixture Injection**: Test receives `task_api_client`, `created_project`, and `db_session`.
2. **Payload Setup**: Generates dynamic title `Task <random_string>`.
3. **Execution**: Calls `task_api_client.create_task(payload)`.
4. **API Assertions**: Validates `status_code == 201`, `response_time < 2.0s`, and JSON Schema matches `TASK_SCHEMA`.
5. **DB Verification**: Queries `get_task_by_id(db_session, task_id)` to confirm row exists in SQLite table with correct title and FK `project_id`.
6. **Teardown**: Fixture automatically issues `DELETE /api/tasks/{id}` after execution.

### Q17: What challenges did you face and how did you resolve them?
**Answer:**
- **Challenge 1**: Inter-test dependency and dirty data causing query count assertions to fail.
  - *Solution*: Implemented Pytest yield fixtures with automatic HTTP teardown and isolated test email generators.
- **Challenge 2**: SQLite threading lock during concurrent test runs.
  - *Solution*: Added `connect_args={"check_same_thread": False}` in SQLAlchemy database setup.
