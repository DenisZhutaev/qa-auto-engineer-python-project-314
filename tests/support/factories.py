from uuid import uuid4


def unique_user(prefix):
    token = uuid4().hex[:8]
    return {
        "email": f"{prefix}_{token}@example.com",
        "first_name": f"{prefix.capitalize()}{token[:4]}",
        "last_name": f"User{token[4:]}",
    }


def unique_status(prefix):
    token = uuid4().hex[:8]
    return {"name": f"{prefix.capitalize()} {token[:4]}", "slug": f"{prefix}-{token}"}


def unique_label(prefix):
    return f"{prefix}-{uuid4().hex[:8]}"


def unique_task(prefix, assignee="john@google.com", status="Draft", label=None):
    token = uuid4().hex[:8]
    return {
        "title": f"{prefix}-task-{token}",
        "content": f"{prefix} content {token}",
        "assignee": assignee,
        "status": status,
        "label": label,
    }
