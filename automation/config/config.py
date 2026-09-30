import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-taskflow-jwt-key-2026")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

    TEST_USER_NAME = os.getenv("TEST_USER_NAME", "QA Tester")
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "qauser@example.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "Test@12345")

    ADMIN_NAME = os.getenv("ADMIN_NAME", "System Admin")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@12345")


config = Config()
