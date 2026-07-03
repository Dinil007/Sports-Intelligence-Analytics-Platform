from __future__ import annotations

from fastapi import APIRouter, Query

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(tags=["Match Momentum"])


@router.get("/match-momentum")
def get_match_momentum(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Match momentum retrieved successfully", analytics_api_service.match_momentum(match_id))