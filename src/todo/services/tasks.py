"""Business rules for tasks. Only this layer calls the repository."""

from dataclasses import dataclass

from todo.repository import tasks as repository

MAX_TITLE = 100
PAGE_SIZE = 20


@dataclass
class ValidationError(ValueError):  # the API turns it into 400 {"error": code, "field": field}
    code: str
    field: str | None = None


def create_task(conn, title, priority):
    title = title.strip()
    return repository.insert(conn, title, priority)


def get_task(conn, task_id):
    return repository.get(conn, task_id)


def list_tasks(conn, done=None, q=None, page=None, size=None):
    if page is None:
        return repository.select(conn, done=done, q=q)
    limit, offset = page_window(page, size)
    return repository.select(conn, done=done, q=q, limit=limit, offset=offset)


def page_window(page, size=None):
    """Return (limit, offset) for one page of results."""
    size = size or PAGE_SIZE
    if page < 1:
        raise ValidationError("invalid_page", "page")
    return size, page * size


def page_count(total, size):
    """How many pages `total` tasks fill."""
    return -(-total // size)


def update_task(conn, task_id, fields):
    return repository.update(conn, task_id, fields)


def delete_task(conn, task_id):
    """Delete a task. Returns False if there was no task with that id."""
    return repository.delete(conn, task_id)
