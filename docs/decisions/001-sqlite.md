# 001: Use SQLite for storage

Status: Accepted (2026-08-03)

## Context

todo-api is a small service with one table and a handful of users. We want
zero set-up for anyone who clones it: no database server, no credentials.

## Decision

Store tasks in SQLite through Python's built-in `sqlite3` module. Schema
changes are numbered SQL files in `migrations/`, applied in filename order on
start-up (`src/todo/db.py`). A migration that is already committed is never
edited; a change gets a new numbered file.

## Consequences

- Nothing to install beyond `requirements.txt`; tests use an in-memory database.
- One writer at a time. Fine at this size; revisit before running more than one
  app instance.
- Moving to Postgres later means porting the SQL in `src/todo/repository/` only,
  because no other layer runs SQL.
