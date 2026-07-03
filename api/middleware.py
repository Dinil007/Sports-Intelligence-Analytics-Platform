from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.logging import elapsed_ms, logger, request_context, timer_start


async def observability_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    start = timer_start()
    context = request_context(request)
    logger.info("request_started", extra=context)
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("request_failed", extra=context)
        raise
    duration = elapsed_ms(start)
    response.headers["X-Execution-Time-ms"] = str(duration)
    logger.info("request_completed", extra={**context, "status_code": response.status_code, "duration_ms": duration})
    return response


async def security_headers_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(observability_middleware)
    app.middleware("http")(security_headers_middleware)