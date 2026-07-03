from __future__ import annotations

from typing import Annotated

from fastapi import Query

from api.utils.pagination import PaginationParams


PageQuery = Annotated[int, Query(ge=1, description="Page number")]
PageSizeQuery = Annotated[int, Query(ge=1, le=100, description="Items per page")]
LimitQuery = Annotated[int, Query(ge=1, le=100, description="Maximum items to return")]


def pagination_params(page: PageQuery = 1, page_size: PageSizeQuery = 25) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)