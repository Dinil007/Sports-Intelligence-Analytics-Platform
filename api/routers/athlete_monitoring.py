from __future__ import annotations

from fastapi import APIRouter

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(tags=["Athlete Monitoring"])


@router.get("/athlete-monitoring")
def get_athlete_monitoring() -> dict[str, object]:
    return success_response("Athlete monitoring retrieved successfully", analytics_api_service.athlete_monitoring())