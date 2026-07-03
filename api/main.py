from __future__ import annotations

from fastapi import FastAPI

from api.config import settings
from api.exceptions import configure_exception_handlers
from api.logging import configure_logging
from api.middleware import configure_middleware
from api.routers import include_routers


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title=settings.title,
        version=settings.version,
        description=settings.description,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    configure_middleware(app)
    configure_exception_handlers(app)
    include_routers(app)
    return app


app = create_app()
