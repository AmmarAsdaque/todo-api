"""Business rules for tasks. Only this layer calls the repository."""

from dataclasses import dataclass
from datetime import date, datetime

from todo.repository import tasks as repository

MAX_TITLE = 100
PAGE_SIZE = 20


@dataclass
class ValidationError(ValueError):  # the API turns it into 400 {"error": code, "field": field}
    code: str
    field: str | None = None


def parse_due(value):
    """YYYY-MM-DD, or None if unreadable."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except Exception:
        return None


def today():
    """Today's date as YYYY-MM-DD. Tests can monkeypatch this."""
    return date.today().isoformat()


def create_task(conn, title, priority, due_date=None):
    # Unreadable due dates are stored as None so the request still succeeds.
    return repository.insert(conn, title.strip(), priority, parse_due(due_date))


def get_task(conn, task_id):
    return repository.get(conn, task_id)


def list_tasks(conn, done=None, q=None, page=None, size=None, overdue=False):
    limit, offset = page_window(page, size) if page is not None else (None, 0)
    before = today() if overdue else None
    return repository.select(
        conn, done=done, q=q, limit=limit, offset=offset, overdue_before=before
    )


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
    if "due_date" in fields:
        # parse_due returns None for unreadable dates, which also clears them
        fields["due_date"] = parse_due(fields["due_date"])
    return repository.update(conn, task_id, fields)
