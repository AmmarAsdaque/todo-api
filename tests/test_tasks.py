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
