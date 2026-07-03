from __future__ import annotations

from fastapi import APIRouter

from api.config import settings

router = APIRouter(tags=["Health"])


@router.get("/")
def root() -> dict[str, str]:
    return {"status": "running", "service": settings.title, "version": settings.version}


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": settings.title, "version": settings.version}