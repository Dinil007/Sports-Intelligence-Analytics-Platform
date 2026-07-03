from __future__ import annotations

from fastapi import APIRouter, Query

from api.dependencies import LimitQuery
from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(prefix="/scouting", tags=["Scouting"])


@router.get("")
def get_scouting(limit: LimitQuery = 25) -> dict[str, object]:
    return success_response("Scouting data retrieved successfully", analytics_api_service.scouting(limit))


@router.get("/search")
def search_scouting(q: str | None = Query(None, min_length=1), limit: LimitQuery = 25) -> dict[str, object]:
    return success_response("Scouting search completed successfully", analytics_api_service.scouting_search(q, limit))


@router.get("/profile")
def get_scouting_profile(player_name: str = Query(..., min_length=1)) -> dict[str, object]:
    return success_response("Scouting profile retrieved successfully", analytics_api_service.scouting_profile(player_name))