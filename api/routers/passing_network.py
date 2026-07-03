from __future__ import annotations

from fastapi import APIRouter, Query

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(tags=["Passing Network"])


@router.get("/passing-network")
def get_passing_network(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Passing network retrieved successfully", analytics_api_service.passing_network(match_id))