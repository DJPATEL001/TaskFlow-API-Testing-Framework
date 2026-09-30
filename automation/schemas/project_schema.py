PROJECT_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "status", "owner_id", "created_at", "updated_at"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "description": {"type": ["string", "null"]},
        "status": {"type": "string"},
        "owner_id": {"type": "integer"},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
    },
    "additionalProperties": False,
}

PROJECT_LIST_SCHEMA = {
    "type": "array",
    "items": PROJECT_SCHEMA,
}
