"""The only module that runs SQL."""


def fetch_all(conn):
    return conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()


def fetch_by_done(conn, done):
    return conn.execute(
        "SELECT id, title, done FROM tasks WHERE done = ? ORDER BY id", (done,)
    ).fetchall()
