from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _field_name(location: tuple) -> str:
    if not location:
        return "field"
    if "body" in location:
        body_index = location.index("body")
        if body_index + 1 < len(location):
            return str(location[body_index + 1])
    return str(location[-1])


def _friendly_message(error: dict) -> str:
    error_type = error.get("type", "")
    field = _field_name(tuple(error.get("loc", ())))

    if field == "email":
        return "Invalid email format"
    if error_type == "missing":
        return f"Missing required field: {field}"
    if error_type in {"string_too_short", "too_short"}:
        return f"{field} is too short"
    if error_type in {"string_too_long", "too_long"}:
        return f"{field} is too long"
    if error_type in {"greater_than_equal", "less_than_equal"} and field == "rating":
        return "Rating must be between 1 and 5"
    if error_type.startswith("int_parsing"):
        return f"{field} must be an integer"
    if error_type.startswith("string_type"):
        return f"{field} must be a string"

    message = error.get("msg", "Invalid request")
    return f"{field}: {message}"


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        del request
        messages = [_friendly_message(error) for error in exc.errors()]
        return JSONResponse(
            status_code=422,
            content={
                "detail": messages[0] if len(messages) == 1 else messages,
            },
        )
