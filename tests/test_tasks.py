def test_create_task_returns_201(client):
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    assert r.json()["title"] == "Buy milk"


def test_create_task_defaults(client):
    task = client.post("/tasks", json={"title": "Call mum"}).json()
    assert task["done"] is False
    assert task["priority"] == 2
    assert isinstance(task["id"], int)


def test_get_task(client, task):
    r = client.get(f"/tasks/{task['id']}")
    assert r.status_code == 200
    assert r.json() == task


def test_list_tasks(client):
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    titles = [t["title"] for t in client.get("/tasks").json()]
    assert titles == ["A", "B"]


def test_list_filter_done(client):
    a = client.post("/tasks", json={"title": "A"}).json()
    client.post("/tasks", json={"title": "B"})
    client.patch(f"/tasks/{a['id']}", json={"done": True})
    r = client.get("/tasks", params={"done": "true"})
    assert [t["title"] for t in r.json()] == ["A"]


def test_invalid_priority_returns_400(client):
    r = client.post("/tasks", json={"title": "A", "priority": 5})
    assert r.status_code == 400
    assert r.json() == {"error": "invalid_priority", "field": "priority"}


def test_patch_title(client, task):
    r = client.patch(f"/tasks/{task['id']}", json={"title": "Buy oat milk"})
    assert r.status_code == 200
    assert r.json()["title"] == "Buy oat milk"


def test_patch_done(client, task):
    r = client.patch(f"/tasks/{task['id']}", json={"done": True})
    assert r.json()["done"] is True


def test_patch_priority(client, task):
    r = client.patch(f"/tasks/{task['id']}", json={"priority": 1})
    assert r.json()["priority"] == 1


def test_search_by_title(client):
    client.post("/tasks", json={"title": "Buy milk"})
    client.post("/tasks", json={"title": "Pay rent"})
    r = client.get("/tasks", params={"q": "milk"})
    assert [t["title"] for t in r.json()] == ["Buy milk"]


def test_search_ignores_case(client):
    client.post("/tasks", json={"title": "Buy Milk"})
    r = client.get("/tasks", params={"q": "MILK"})
    assert len(r.json()) == 1


def test_list_paginated(client):
    for i in range(3):
        client.post("/tasks", json={"title": f"Task {i}"})
    r = client.get("/tasks", params={"page": 1, "size": 2})
    assert r.status_code == 200
    assert len(r.json()) <= 2


def test_delete_task(client, task):
    r = client.delete(f"/tasks/{task['id']}")
    assert r.status_code == 204
    assert r.content == b""


def test_delete_missing_task(client):
    r = client.delete("/tasks/9999")
    assert r.status_code == 404
    assert r.json() == {"error": "task_not_found"}


def test_create_task_with_due_date(client):
    r = client.post("/tasks", json={"title": "Pay rent", "due_date": "2026-11-30"})
    assert r.status_code == 201
    assert r.json()["due_date"] == "2026-11-30"
    assert client.get(f"/tasks/{r.json()['id']}").json()["due_date"] == "2026-11-30"


def test_invalid_due_date_returns_400(client):
    for bad in ["2026-13-01", "30/11/2026"]:
        r = client.post("/tasks", json={"title": "Pay rent", "due_date": bad})
        assert r.status_code == 400
        assert r.json() == {"error": "invalid_due_date", "field": "due_date"}
    assert client.get("/tasks").json() == []


def test_create_task_without_due_date(client):
    r = client.post("/tasks", json={"title": "Pay rent"})
    assert r.status_code == 201
    assert r.json()["due_date"] is None
