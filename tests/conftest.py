import sqlite3

import pytest


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, done INTEGER)")
    connection.executemany(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        [(1, "Buy milk", 0), (2, "Pay rent", 1), (3, "Call mum", 0)],
    )
    yield connection
    connection.close()
