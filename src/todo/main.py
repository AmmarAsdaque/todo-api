from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from todo.routes import tasks as task_routes
from todo.services.tasks import ValidationError

app = FastAPI(title="todo-api", version="0.3.0")
app.include_router(task_routes.router)


@app.exception_handler(ValidationError)
def validation_error(request: Request, exc: ValidationError):
    body = {"error": exc.code}
    if exc.field:
        body["field"] = exc.field
    return JSONResponse(status_code=400, content=body)


@app.exception_handler(RequestValidationError)
def bad_request(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    loc = errors[0]["loc"] if errors else ()
    if len(loc) < 2:
        return JSONResponse(status_code=400, content={"error": "invalid_request"})
    field = str(loc[-1])
    return JSONResponse(status_code=400, content={"error": f"invalid_{field}", "field": field})
