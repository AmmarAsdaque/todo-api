import pytest
from fastapi.testclient import TestClient

from todo.db import connect, get_conn
from todo.main import app


@pytest.fixture
def conn():
    connection = connect(":memory:")
    yield connection
    connection.close()


@pytest.fixture
def client(conn):
    app.dependency_overrides[get_conn] = lambda: conn
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def task(client):
    return client.post("/tasks", json={"title": "Buy milk"}).json()
