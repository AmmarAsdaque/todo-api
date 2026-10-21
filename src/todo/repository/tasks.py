"""SQLite access for tasks. The only module that runs SQL."""

COLUMNS = "id, title, done, priority, created_at, due_date"


def to_task(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "priority": row["priority"],
        "created_at": row["created_at"],
        "due_date": row["due_date"],
    }


def insert(conn, title, priority, due_date=None):
    with conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, priority, due_date, created_at) "
            "VALUES (?, ?, ?, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))",
            (title, priority, due_date),
        )
    return get(conn, cur.lastrowid)


def get(conn, task_id):
    row = conn.execute(f"SELECT {COLUMNS} FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return to_task(row)


def select(conn, done=None, q=None, limit=None, offset=0, overdue_before=None):
    """overdue_before: only open tasks with a due date before this YYYY-MM-DD."""
    sql = f"SELECT {COLUMNS} FROM tasks"
    where, params = [], []
    if done is not None:
        where.append("done = ?")
        params.append(int(done))
    if q:
        where.append("title LIKE ?")
        params.append(f"%{q}%")
    if overdue_before is not None:
        where.append("done = 0")
        where.append("due_date IS NOT NULL")
        where.append("due_date < ?")
        params.append(overdue_before)
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY id"
    if limit is not None:
        sql += " LIMIT ? OFFSET ?"
        params += [limit, offset]
    return [to_task(row) for row in conn.execute(sql, params)]


def update(conn, task_id, fields):
    if fields:
        assignments = ", ".join(f"{name} = ?" for name in fields)
        with conn:
            conn.execute(
                f"UPDATE tasks SET {assignments} WHERE id = ?",
                (*fields.values(), task_id),
            )
    return get(conn, task_id)
