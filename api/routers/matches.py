from __future__ import annotations

from fastapi import APIRouter, Depends

from api.dependencies import LimitQuery, pagination_params
from api.responses import success_response
from api.services import match_api_service
from api.utils.pagination import PaginationParams
from api.utils.validators import validate_positive_id

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("")
def get_matches(params: PaginationParams = Depends(pagination_params)) -> dict[str, object]:
    return success_response("Matches retrieved successfully", match_api_service.list_matches(params.page, params.page_size))


@router.get("/recent")
def get_recent_matches(limit: LimitQuery = 10) -> dict[str, object]:
    return success_response("Recent matches retrieved successfully", match_api_service.recent_matches(limit))


@router.get("/{match_id}")
def get_match(match_id: int) -> dict[str, object]:
    return success_response("Match retrieved successfully", match_api_service.get_match(validate_positive_id(match_id, "match_id")))