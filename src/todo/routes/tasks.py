from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from todo.db import get_conn
from todo.services import tasks

router = APIRouter()


class TaskIn(BaseModel):
    title: str
    priority: int = Field(default=2, ge=1, le=3)
    due_date: str | None = None


class TaskPatch(BaseModel):
    title: str | None = None
    done: bool | None = None
    priority: int | None = Field(default=None, ge=1, le=3)
    due_date: str | None = None


@router.post("/tasks", status_code=201)
def create(body: TaskIn, conn=Depends(get_conn)):
    return tasks.create_task(conn, body.title, body.priority, body.due_date)


@router.get("/tasks")
def list_all(
    done: bool | None = None,
    q: str | None = None,
    page: int | None = None,
    size: int | None = None,
    overdue: bool = False,
    conn=Depends(get_conn),
):
    """List tasks. ?overdue=true lists open tasks due before today."""
    return tasks.list_tasks(conn, done=done, q=q, page=page, size=size, overdue=overdue)


@router.get("/tasks/{task_id}")
def get_one(task_id: int, conn=Depends(get_conn)):
    return tasks.get_task(conn, task_id)


@router.patch("/tasks/{task_id}")
def patch(task_id: int, body: TaskPatch, conn=Depends(get_conn)):
    fields = body.model_dump(exclude_unset=True)
    if "title" in fields:
        fields["title"] = fields["title"].strip()
    return tasks.update_task(conn, task_id, fields)
