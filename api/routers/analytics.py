from __future__ import annotations

from fastapi import APIRouter, Query

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/player")
def get_player_analytics(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Player analytics retrieved successfully", analytics_api_service.player_analytics(match_id))


@router.get("/team")
def get_team_analytics(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Team analytics retrieved successfully", analytics_api_service.team_analytics(match_id))


@router.get("/match")
def get_match_analytics(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Match analytics retrieved successfully", analytics_api_service.match_analytics(match_id))