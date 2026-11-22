MAX_TITLE = 100


class ValidationError(ValueError):
    pass


def validate_title(title):
    title = title.strip()
    if len(title) == 0:
        raise ValidationError("title is required")
    if len(title) > MAX_TITLE:
        raise ValidationError("title too long")
    return title


def add_task(store, title, priority=2):
    title = validate_title(title)
    if priority < 1 or priority > 3:
        raise ValidationError("priority must be 1-3")
    task = {"id": len(store) + 1, "title": title, "priority": priority, "done": False}
    store.append(task)
    return task


def list_tasks(store, min_priority=1):
    return [t for t in store if t["priority"] >= min_priority and not t["done"]]
