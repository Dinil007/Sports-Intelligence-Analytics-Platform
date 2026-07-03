from __future__ import annotations

from fastapi import HTTPException


def validate_positive_id(value: int, field_name: str = "id") -> int:
    if value < 1:
        raise HTTPException(status_code=400, detail=f"{field_name} must be a positive integer")
    return value


def validate_limit(limit: int, max_limit: int = 100) -> int:
    if limit < 1 or limit > max_limit:
        raise HTTPException(status_code=400, detail=f"limit must be between 1 and {max_limit}")
    return limit


def validate_sort(sort: str | None, allowed: set[str]) -> str | None:
    if sort and sort not in allowed:
        raise HTTPException(status_code=400, detail=f"sort must be one of: {', '.join(sorted(allowed))}")
    return sort