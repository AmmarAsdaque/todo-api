from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from todo.db import get_conn
from todo.services import tasks

router = APIRouter()


class TaskIn(BaseModel):
    title: str
    priority: int = Field(default=2, ge=1, le=3)


class TaskPatch(BaseModel):
    title: str | None = None
    done: bool | None = None
    priority: int | None = Field(default=None, ge=1, le=3)


@router.post("/tasks", status_code=201)
def create(body: TaskIn, conn=Depends(get_conn)):
    return tasks.create_task(conn, body.title, body.priority)


@router.get("/tasks")
def list_all(
    done: bool | None = None,
    q: str | None = None,
    page: int | None = None,
    size: int | None = None,
    conn=Depends(get_conn),
):
    return tasks.list_tasks(conn, done=done, q=q, page=page, size=size)


@router.get("/tasks/{task_id}")
def get_one(task_id: int, conn=Depends(get_conn)):
    return tasks.get_task(conn, task_id)


@router.patch("/tasks/{task_id}")
def patch(task_id: int, body: TaskPatch, conn=Depends(get_conn)):
    fields = body.model_dump(exclude_none=True)
    if "title" in fields:
        fields["title"] = fields["title"].strip()
    return tasks.update_task(conn, task_id, fields)


@router.delete("/tasks/{task_id}")
def delete(task_id: int, conn=Depends(get_conn)):
    task = tasks.get_task(conn, task_id)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return {"deleted": True, "task": task}
