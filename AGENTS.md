# AGENTS.md

todo-api: a small REST API for to-do tasks. Python 3.12, FastAPI, SQLite.

## Commands

- Set up: `python -m venv .venv && source .venv/bin/activate`
- Install: `pip install -r requirements.txt`
- Run all tests: `pytest -q`
- Run one test file: `pytest -q tests/test_tasks.py`
- Lint: `ruff check .`
- Format: `ruff format .`
- Run locally: `uvicorn todo.main:app --reload`

Run `pytest -q` and `ruff check .` before saying a task is done.
Do not run tests with `-v`; the output is long and not needed.

## Project layout

- `src/todo/main.py` creates the app and includes the routers
- `src/todo/routes/tasks.py` HTTP layer (FastAPI routers); keep handlers thin
- `src/todo/services/tasks.py` business rules (for example `MAX_TITLE = 100`)
- `src/todo/services/pagination.py` `parse_pagination`
- `src/todo/repository/tasks.py` SQLite access
- `src/todo/utils/dates.py` `parse_date`
- `migrations/` numbered SQL files, applied in order
- `tests/test_tasks.py` API tests; `tests/test_architecture.py` layer rules
- `specs/` specs for changes; `PROGRESS.md` progress notes for long sessions

## Conventions

- Dates are ISO 8601 date strings (YYYY-MM-DD), never numbers; parse with `parse_date`
- IDs are integers from the database; never generate them in code
- Every new behaviour gets a test in `tests/test_tasks.py`
- Error responses use the shape `{"error": "<code>", "field": "<name>"}`; `field` is optional, set it when one input field is at fault
- Repeatable procedures live in `.agents/skills/`; use `add-endpoint` when adding a route

## Boundaries

- Only `services/` may import `repository/`; routes never touch the database
- Never edit files in `migrations/` that are already committed; add a new numbered file
- Never commit `.env` or anything with keys or passwords
- Ask before adding a dependency to `requirements.txt`
- Ask before deleting or renaming a public endpoint
- Do not change tests to make them pass; fix the code or ask

## Known failure patterns

- Ran `python -m unittest` and found no tests: use `pytest -q`
- Put SQL in a route handler: move it to `repository/` and call it from `services/`
- Wrote dates as Unix timestamps: use YYYY-MM-DD strings
- Why SQLite and not Postgres: see `docs/decisions/001-sqlite.md` (background only)
