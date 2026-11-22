from todo.services import tasks as task_service


def get_tasks(conn):
    return task_service.list_tasks(conn)
