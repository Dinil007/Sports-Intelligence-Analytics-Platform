from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    data: T | None = None
    timestamp: str


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    data: Any | None = None
    timestamp: str


class PaginationResponse(BaseModel):
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)
    total: int = Field(..., ge=0)
    pages: int = Field(..., ge=0)


class PaginatedData(BaseModel):
    items: list[Any]
    pagination: PaginationResponse