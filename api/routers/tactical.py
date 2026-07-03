from __future__ import annotations

from fastapi import APIRouter, Query

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(prefix="/tactical", tags=["Tactical Analysis"])


@router.get("")
def get_tactical(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    return success_response("Tactical analysis retrieved successfully", analytics_api_service.tactical(match_id))


@router.get("/summary")
def get_tactical_summary(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    data = analytics_api_service.tactical(match_id)
    return success_response("Tactical summary retrieved successfully", data.get("summary", data))


@router.get("/verdict")
def get_tactical_verdict(match_id: int = Query(1, ge=1)) -> dict[str, object]:
    data = analytics_api_service.tactical(match_id)
    return success_response("Tactical verdict retrieved successfully", data.get("verdict", data))