import json
import os
import random
import string


def generate_random_email(prefix: str = "qa_user") -> str:
    """Generate a unique email address for dynamic test isolation."""
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{random_str}@example.com"


def generate_random_string(length: int = 10) -> str:
    """Generate a random string of fixed length."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def load_test_data() -> dict:
    """Load static test payloads from automation/test_data/test_data.json."""
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "test_data",
        "test_data.json",
    )
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
