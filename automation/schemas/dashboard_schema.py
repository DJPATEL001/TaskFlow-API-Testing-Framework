DASHBOARD_SCHEMA = {
    "type": "object",
    "required": [
        "total_projects",
        "total_tasks",
        "completed_tasks",
        "pending_tasks",
        "high_priority_tasks",
    ],
    "properties": {
        "total_projects": {"type": "integer"},
        "total_tasks": {"type": "integer"},
        "completed_tasks": {"type": "integer"},
        "pending_tasks": {"type": "integer"},
        "high_priority_tasks": {"type": "integer"},
    },
    "additionalProperties": False,
}
