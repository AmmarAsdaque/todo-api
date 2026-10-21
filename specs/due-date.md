# Spec: optional due dates on tasks

## Goal
Users can give a task an optional due date and list the tasks that are overdue,
so they can see what needs attention first.

## Acceptance criteria
1. POST /tasks with "due_date": "2026-11-30" returns 201, and the response and a
   later GET /tasks/{id} both include "due_date": "2026-11-30".
2. POST /tasks without due_date returns 201 with "due_date": null.
3. POST /tasks with "due_date": "2026-13-01" or "30/11/2026" returns 400 with body
   {"error": "invalid_due_date", "field": "due_date"}, and no task is saved.
4. GET /tasks?overdue=true returns only tasks where done is false and due_date is
   before today. Tasks with no due date are never overdue. In tests, today is fixed
   to 2026-11-15.
5. PATCH /tasks/{id} with "due_date": null clears the date.
6. GET /tasks without the overdue parameter returns the same tasks, in the same
   order, as before this change.

## Constraints
- No new dependencies.
- Only these files change: src/todo/services/tasks.py, src/todo/routes/tasks.py,
  src/todo/repository/tasks.py, one new file in migrations/, tests/test_tasks.py.
- Existing response fields keep their names and types.
- All existing tests pass without being edited.
- Dates are stored and returned as ISO 8601 date strings (YYYY-MM-DD).

## Non-goals
- Time zones or times of day.
- Reminders or notifications.
- Recurring tasks.
- Changes to any client app.
