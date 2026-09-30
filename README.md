# TaskFlow API - REST API Testing Automation Framework

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Test Framework](https://img.shields.io/badge/Pytest-8.0%2B-red.svg)](https://docs.pytest.org/)
[![Reports](https://img.shields.io/badge/pytest--html-Report%20Generated-brightgreen.svg)](reports/api_test_report.html)

> TaskFlow API is a REST API testing project demonstrating manual API testing and automated API testing using Python, Pytest and Requests.

---

## 📌 Project Overview

This repository contains a complete, production-grade **REST API Automation Testing Framework** built for **TaskFlow API** — a task and project management backend service. The repository includes both the realistic backend API application and a complete testing framework covering manual test design, automated Pytest test suites, database verification, Postman collection test scripts, and HTML test reports.

---

## 🛠️ Technology Stack

- **Backend Application**: Python 3.11+, FastAPI, SQLAlchemy, SQLite (MySQL compatible), Pydantic v2, PyJWT, Passlib/Bcrypt, Uvicorn
- **Automated Testing Framework**: Pytest, Requests, Pytest-HTML, JSONSchema, Python-Dotenv
- **Manual & Exploration Testing**: Postman v10+, Swagger UI, ReDoc, OpenPyXL
- **Database & Persistence**: SQLite3 (`taskflow.db`), SQLAlchemy ORM

---

## 🏗️ Architecture

```text
       +-------------------------------------------------------+
       |                  Pytest Test Suite                    |
       |  (test_auth, test_projects, test_tasks, test_users)   |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |                    API Client Layer                   |
       |  (AuthClient, ProjectClient, TaskClient, UserClient)  |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |                   Python Requests                     |
       +---------------------------+---------------------------+
                                   | HTTP / Bearer JWT Token
                                   v
       +-------------------------------------------------------+
       |                  TaskFlow REST API                    |
       |              (FastAPI + Uvicorn Server)               |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |             Database & Assertions Layer               |
       |    (SQLAlchemy Direct Queries & HTML Test Reports)    |
       +-------------------------------------------------------+
```

---

## 📁 Repository Structure

```text
TaskFlow-API-Testing-Framework/
│
├── app/                        # FastAPI Backend Application
│   ├── main.py                 # FastAPI Application entry point & router inclusion
│   ├── database.py             # SQLAlchemy Engine, SessionLocal & Base
│   ├── seed.py                 # Initial Database Seed Script (Admin, QA User, Data)
│   ├── models/                 # SQLAlchemy DB Models (User, Project, Task)
│   ├── schemas/                # Pydantic Schemas for Request/Response validation
│   ├── services/               # Auth Security, Hashing & JWT dependencies
│   └── routers/                # API Endpoints (auth, projects, tasks, users, dashboard)
│
├── automation/                 # Python Pytest Automation Framework
│   ├── config/                 # Config loader (.env handling)
│   ├── clients/                # Reusable API Client Layer (BaseClient, AuthClient, etc.)
│   ├── schemas/                # JSON Schemas for response contract validation
│   ├── test_data/              # Static test data & edge case JSON payloads
│   ├── tests/                  # Automated Pytest Test Suite (45 Tests)
│   │   ├── test_auth.py
│   │   ├── test_projects.py
│   │   ├── test_tasks.py
│   │   ├── test_users.py
│   │   └── test_dashboard.py
│   ├── utils/                  # Reusable Helpers (api_helpers, assertions, db_helpers)
│   ├── conftest.py             # Pytest Fixtures (auth_token, clients, tear-down)
│   ├── pytest.ini              # Pytest Configuration
│   └── requirements.txt        # Automation dependencies
│
├── manual_testing/             # Manual Testing Deliverables
│   ├── API_Test_Plan.md        # Comprehensive API Test Plan
│   ├── API_Test_Cases.xlsx     # 52 Executed Manual API Test Cases (Excel format)
│   └── API_Bug_Reports.md      # 5 Realistic API Bug Reports
│
├── Postman/                    # Postman Collection & Environment
│   ├── TaskFlow_API.postman_collection.json
│   └── TaskFlow_Local.postman_environment.json
│
├── docs/                       # Interview Preparation
│   └── interview_questions.md  # Q&A guide tailored for QA Automation / SDET roles
│
├── reports/                    # Test Execution Output
│   └── api_test_report.html    # Pytest HTML Test Execution Report
│
├── .env.example                # Environment Variable Template
├── .gitignore                  # Git Ignore Definitions
├── requirements.txt            # Project Dependencies
└── README.md                   # Project Documentation
```

---

## ⚡ Installation & Local Setup

### 1. Clone Repository & Setup Virtual Environment

```bash
git clone https://github.com/DJPATEL001/TaskFlow-API-Testing-Framework.git
cd TaskFlow-API-Testing-Framework

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed Database

```bash
python -m app.seed
```

---

## 🚀 Running the API Application

Start the TaskFlow FastAPI server locally:

```bash
uvicorn app.main:app --reload
```

Interactive API documentation will be accessible at:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 🧪 Executing Automated Tests

Ensure the API server is running on `http://127.0.0.1:8000`, then execute the Pytest suite:

```bash
# Run all automated tests
pytest

# Run tests and generate HTML Execution Report
pytest --html=reports/api_test_report.html --self-contained-html
```

---

## 📮 Postman Collection Usage

1. Open **Postman**.
2. Import `Postman/TaskFlow_API.postman_collection.json`.
3. Import `Postman/TaskFlow_Local.postman_environment.json`.
4. Select `TaskFlow Local` environment.
5. Send request `Authentication -> Login`. The JWT token will automatically be stored in `{{access_token}}`.
6. Run the full collection using **Postman Collection Runner**.

---

## 📊 Final Test Metrics & Coverage Summary

| Metric | Target | Actual Count | Status |
| :--- | :---: | :---: | :---: |
| **Manual API Test Cases** | 50+ | **52** | ✅ Complete |
| **Automated API Pytest Tests** | 40+ | **45** | ✅ 100% Passed |
| **Postman API Requests** | 15+ | **16** | ✅ Complete |
| **API Bug Reports** | 5+ | **5** | ✅ Complete |

---

## 💡 Key Testing Features Demonstrated

- **API Client Layer Pattern**: Clean separation of API call wrappers from test assertions.
- **Pytest Fixture Lifecycle**: Session & function scoped fixtures for token reuse, client setup, and dynamic test data teardown.
- **Database Verification**: Direct SQLAlchemy queries to verify persistence and foreign key cascades.
- **Robust Negative Testing**: Input validations, enum checks, duplicate checks, 401/403/404/422 status assertions.
- **Response Validation**: Structural JSON Schema validation and response timing sanity bounds.
