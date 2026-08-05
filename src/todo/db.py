"""SQLite connection and migrations."""

import os
import sqlite3
from pathlib import Path

MIGRATIONS = Path(__file__).resolve().parents[2] / "migrations"
DB_PATH = os.environ.get("TODO_DB", "todo.db")

_conn = None


def connect(path=None):
    conn = sqlite3.connect(path or DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    migrate(conn)
    return conn


def migrate(conn):
    """Apply every file in migrations/ that has not run yet, in filename order.

    Each file runs in one transaction: if it fails halfway, none of it is kept.
    """
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY)")
    applied = {row[0] for row in conn.execute("SELECT name FROM schema_migrations")}
    for path in sorted(MIGRATIONS.glob("*.sql")):
        if path.name in applied:
            continue
        script = path.read_text(encoding="utf-8")
        try:
            conn.executescript(
                "BEGIN;\n"
                + script
                + f"\nINSERT INTO schema_migrations (name) VALUES ('{path.name}');\nCOMMIT;"
            )
        except sqlite3.Error:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise


def get_conn():
    """FastAPI dependency: one shared connection for the app."""
    global _conn
    if _conn is None:
        _conn = connect()
    return _conn
