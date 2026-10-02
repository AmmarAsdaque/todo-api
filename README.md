# todo-api

A small REST API for to-do tasks. Python, FastAPI and SQLite.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the tests

```bash
pytest -q
```

A fresh copy reports `12 passed`.

## Lint

```bash
ruff check .
```

## Run locally

```bash
uvicorn todo.main:app --reload
```

The API listens on http://localhost:8000. The database file is `todo.db` in the
folder you start it from (set `TODO_DB` to use another path). Migrations in
`migrations/` are applied in filename order on start-up.

## Endpoints

| Method | Path | Notes |
| --- | --- | --- |
| POST | `/tasks` | body `{"title": "...", "priority": 1-3}`; returns 201 |
| GET | `/tasks` | `?done=true/false`, `?q=` title search, `?page=&size=` |
| GET | `/tasks/{id}` | one task |
| PATCH | `/tasks/{id}` | any of `title`, `done`, `priority` |

Errors use the shape `{"error": "<code>", "field": "<name>"}` with status 400.

## Layout

```
src/todo/
  main.py            app, routers, error handlers
  db.py              SQLite connection and migrations
  routes/            HTTP layer
  services/          business rules
  repository/        SQL (the only code that talks to the database)
  utils/             small helpers
migrations/          numbered SQL files
tests/               pytest
docs/                decisions and project history
```

## Project history

Issues, pull requests and releases are listed in
[docs/history/README.md](docs/history/README.md).
