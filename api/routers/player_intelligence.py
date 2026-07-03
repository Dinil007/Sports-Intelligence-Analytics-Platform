from __future__ import annotations

from fastapi import APIRouter, Query

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(tags=["Player Intelligence"])


@router.get("/player-intelligence")
def get_player_intelligence(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Player intelligence retrieved successfully", analytics_api_service.player_intelligence(match_id))