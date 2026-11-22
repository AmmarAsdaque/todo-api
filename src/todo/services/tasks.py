from todo.repository import tasks as task_repo


def list_tasks(conn):
    return task_repo.fetch_all(conn)
