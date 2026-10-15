"""SQLite access for tasks. The only module that runs SQL."""

COLUMNS = "id, title, done, priority, created_at"


def to_task(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
        "priority": row["priority"],
        "created_at": row["created_at"],
    }


def insert(conn, title, priority):
    with conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, priority, created_at) "
            "VALUES (?, ?, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))",
            (title, priority),
        )
    return get(conn, cur.lastrowid)


def get(conn, task_id):
    row = conn.execute(f"SELECT {COLUMNS} FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return to_task(row)


def select(conn, done=None, q=None, limit=None, offset=0):
    sql = f"SELECT {COLUMNS} FROM tasks"
    where, params = [], []
    if done is not None:
        where.append("done = ?")
        params.append(int(done))
    if q:
        where.append("title LIKE ?")
        params.append(f"%{q}%")
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


# --- tags (work in progress) ---


def add_tag(conn, task_id, name):
    with conn:
        conn.execute("INSERT OR IGNORE INTO tags (task_id, name) VALUES (?, ?)", (task_id, name))


def tags_for(conn, task_id):
    rows = conn.execute("SELECT name FROM tags WHERE task_id = ? ORDER BY name", (task_id,))
    return [row["name"] for row in rows]
