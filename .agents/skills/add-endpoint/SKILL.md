---
name: add-endpoint
description: Adds a REST endpoint to the to-do API with route, service logic and tests. Use when the user asks to add, create or expose an endpoint, route or API method.
---

# Add an endpoint

## Steps

1. Write the test first in `tests/test_tasks.py`. Cover the success case
   and one error case. Run `pytest -q tests/test_tasks.py`; the new test
   must fail.
2. Put the rule in `src/todo/services/tasks.py`. Only the service may call
   `src/todo/repository/tasks.py`; `tests/test_architecture.py` checks this.
3. Add a thin handler in `src/todo/routes/tasks.py` that calls the service.
4. Use these status codes:
   - create: 201 with the new object
   - read, update: 200 with the object
   - delete: 204 with no body
   - not found: 404 with `{"error": "task_not_found"}`
5. Run `pytest -q` and `ruff check .`. Fix every failure.
6. Reply with: the endpoint added, the tests added, and the test result line.

## Example test

    def test_delete_task(client, task):
        r = client.delete(f"/tasks/{task['id']}")
        assert r.status_code == 204
        assert r.content == b""

## Edge cases

- Missing id returns 404, not 500.
- For other error responses, read `references/errors.md`.
