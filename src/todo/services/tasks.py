"""Business rules for tasks. Only this layer calls the repository."""

from dataclasses import dataclass
from datetime import date

from todo.repository import tasks as repository
from todo.utils.dates import parse_date

MAX_TITLE = 100
PAGE_SIZE = 20


@dataclass
class ValidationError(ValueError):  # the API turns it into 400 {"error": code, "field": field}
    code: str
    field: str | None = None


def check_due(value):
    """YYYY-MM-DD or None. Any other value is a 400 invalid_due_date (spec AC3)."""
    if value is None:
        return None
    try:
        return parse_date(value).isoformat()
    except ValueError:
        raise ValidationError("invalid_due_date", "due_date") from None


def today():
    """Today's date as YYYY-MM-DD. Tests can monkeypatch this."""
    return date.today().isoformat()


def create_task(conn, title, priority, due_date=None):
    return repository.insert(conn, title.strip(), priority, check_due(due_date))


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
        fields["due_date"] = check_due(fields["due_date"])
    return repository.update(conn, task_id, fields)
