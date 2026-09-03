"""Business rules for tasks. Only this layer calls the repository."""

from todo.repository import tasks as repository

MAX_TITLE = 100


def create_task(conn, title, priority):
    title = title.strip()
    return repository.insert(conn, title, priority)


def get_task(conn, task_id):
    return repository.get(conn, task_id)


def list_tasks(conn, done=None, q=None):
    return repository.select(conn, done=done, q=q)


def update_task(conn, task_id, fields):
    return repository.update(conn, task_id, fields)
