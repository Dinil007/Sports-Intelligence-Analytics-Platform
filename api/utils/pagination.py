from __future__ import annotations

from math import ceil
from typing import Any

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(25, ge=1, le=100)


def paginate(items: list[Any], params: PaginationParams) -> dict[str, Any]:
    total = len(items)
    pages = ceil(total / params.page_size) if total else 0
    start = (params.page - 1) * params.page_size
    end = start + params.page_size
    return {"items": items[start:end], "page": params.page, "page_size": params.page_size, "total": total, "pages": pages}