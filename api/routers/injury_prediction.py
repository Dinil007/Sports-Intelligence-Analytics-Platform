from __future__ import annotations

from fastapi import APIRouter

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(tags=["Injury Risk"])


@router.get("/injury-risk")
def get_injury_risk() -> dict[str, object]:
    return success_response("Injury risk retrieved successfully", analytics_api_service.injury_risk())