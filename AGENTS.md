# AGENTS.md

todo-api: a small to-do API. Python 3.10+, pytest, SQLite.

## Commands
- Run all tests: `pytest -q` (run from the repo root)

## Project layout
- `src/todo/routes/tasks.py` request handlers
- `src/todo/services/tasks.py` logic
- `src/todo/repository/tasks.py` SQL
- `tests/conftest.py` builds an in-memory database with three tasks

## Boundaries
- routes/ call services/ only.
- Only repository/ may touch the database.
