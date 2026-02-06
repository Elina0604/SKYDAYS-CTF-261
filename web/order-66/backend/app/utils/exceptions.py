from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VaderTodoException(Exception):
    """Base exception for Vader Todo API"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TodoNotFoundError(VaderTodoException):
    """Exception raised when a todo is not found"""
    def __init__(self, todo_id: str):
        super().__init__(f"Todo with ID '{todo_id}' not found", 404)


class PreferencesError(VaderTodoException):
    """Exception raised for preferences-related errors"""
    def __init__(self, message: str):
        super().__init__(f"Preferences error: {message}", 400)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with Vader-themed messages"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Your lack of proper input is disturbing.",
            "errors": errors,
            "vader_quote": "I find your lack of faith disturbing."
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with Vader-themed messages"""
    vader_quotes = {
        404: "I find your search... lacking.",
        400: "Your request has failed me for the last time.",
        422: "Your lack of proper input is disturbing.",
        500: "The Emperor is not as forgiving as I am.",
        403: "You do not yet realize your importance.",
        401: "You have failed me for the last time."
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "vader_quote": vader_quotes.get(exc.status_code, "The Force is not strong with this request.")
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred",
            "vader_quote": "The Emperor is not as forgiving as I am."
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "vader_quote": "I have you now."
        }
    )