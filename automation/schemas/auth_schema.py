USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "role", "created_at"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "role": {"type": "string"},
        "created_at": {"type": "string"},
    },
    "additionalProperties": False,
}

LOGIN_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["access_token", "token_type", "user"],
    "properties": {
        "access_token": {"type": "string"},
        "token_type": {"type": "string"},
        "user": USER_SCHEMA,
    },
    "additionalProperties": False,
}
