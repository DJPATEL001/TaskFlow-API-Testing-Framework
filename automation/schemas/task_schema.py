TASK_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "priority", "status", "project_id", "created_at", "updated_at"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "description": {"type": ["string", "null"]},
        "priority": {"type": "string"},
        "status": {"type": "string"},
        "project_id": {"type": "integer"},
        "assigned_to": {"type": ["integer", "null"]},
        "due_date": {"type": ["string", "null"]},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
    },
    "additionalProperties": False,
}

TASK_LIST_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["items", "total", "page", "limit", "pages"],
    "properties": {
        "items": {
            "type": "array",
            "items": TASK_SCHEMA,
        },
        "total": {"type": "integer"},
        "page": {"type": "integer"},
        "limit": {"type": "integer"},
        "pages": {"type": "integer"},
    },
    "additionalProperties": False,
}
