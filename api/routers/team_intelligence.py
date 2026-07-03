from __future__ import annotations

from fastapi import APIRouter, Query

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(tags=["Team Intelligence"])


@router.get("/team-intelligence")
def get_team_intelligence(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Team intelligence retrieved successfully", analytics_api_service.team_intelligence(match_id))