# Error responses in todo-api

Every error body has the same shape:

    {"error": "<code>", "field": "<name>"}

`field` is optional: set it when one input field is at fault.

| Status | When | Example body |
| --- | --- | --- |
| 400 | Bad input in the request | `{"error": "invalid_priority", "field": "priority"}` |
| 404 | The task id does not exist | `{"error": "task_not_found"}` |

Rules

- Bad input is 400, never 422. `src/todo/main.py` turns request validation
  errors into 400 with `invalid_<field>` as the code.
- Codes are snake_case: `invalid_<field>` for bad input, `<thing>_not_found`
  for a missing record.
- For a rule the request model cannot express, raise
  `ValidationError(code, field)` in `src/todo/services/`; `src/todo/main.py`
  turns it into a 400 with that body.
- Never put an exception message or a stack trace in the body.
- Test the status code and the exact body.
