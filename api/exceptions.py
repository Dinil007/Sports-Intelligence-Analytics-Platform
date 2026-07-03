from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.logging import logger, request_context
from api.responses import error_response


def _json(status_code: int, message: str, data: object = None) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=error_response(message=message, data=data))


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return _json(exc.status_code, str(exc.detail))


async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    message = "Resource not found" if exc.status_code == 404 else str(exc.detail)
    return _json(exc.status_code, message)


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _json(422, "Validation failed", exc.errors())


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return _json(400, "Invalid request data", exc.errors())


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled_exception", extra=request_context(request))
    return _json(500, "Internal server error")


def configure_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)