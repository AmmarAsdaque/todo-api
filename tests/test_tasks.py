import pytest
from todo.services.tasks import add_task, list_tasks, ValidationError


def test_add_task_returns_task():
    store = []
    task = add_task(store, "Buy milk")
    assert task is not None
    assert len(store) == 1


def test_empty_title_rejected():
    with pytest.raises(ValidationError):
        add_task([], "   ")


def test_list_tasks():
    store = []
    add_task(store, "A", priority=3)
    add_task(store, "B", priority=1)
    assert len(list_tasks(store)) > 0
