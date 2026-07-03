from __future__ import annotations

from typing import Any

from api.utils.pagination import PaginationParams, paginate
from api.utils.serialization import serialize


def list_matches(page: int = 1, page_size: int = 25) -> dict[str, Any]:
    matches = [{"id": index, "label": f"Match {index}"} for index in range(1, 101)]
    return paginate(matches, PaginationParams(page=page, page_size=page_size))


def get_match(match_id: int) -> dict[str, Any]:
    from services.match_intelligence_service import get_match_dashboard

    return serialize(get_match_dashboard(match_id))


def recent_matches(limit: int = 10) -> list[dict[str, Any]]:
    return [{"id": index, "label": f"Recent Match {index}"} for index in range(1, limit + 1)]