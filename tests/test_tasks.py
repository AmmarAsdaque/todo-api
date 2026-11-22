from todo.repository import tasks as task_repo
from todo.routes.tasks import get_tasks
from todo.services import tasks as task_service


def test_fetch_all_returns_every_task(conn):
    assert len(task_repo.fetch_all(conn)) == 3


def test_fetch_by_done_filters(conn):
    assert task_repo.fetch_by_done(conn, 1) == [(2, "Pay rent", 1)]
    assert [row[0] for row in task_repo.fetch_by_done(conn, 0)] == [1, 3]


def test_service_lists_all_tasks(conn):
    assert task_service.list_tasks(conn) == task_repo.fetch_all(conn)


def test_get_tasks_lists_all_tasks(conn):
    assert [row[1] for row in get_tasks(conn)] == ["Buy milk", "Pay rent", "Call mum"]


def test_tasks_are_ordered_by_id(conn):
    assert [row[0] for row in get_tasks(conn)] == [1, 2, 3]
