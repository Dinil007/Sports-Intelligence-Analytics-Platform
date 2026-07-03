from __future__ import annotations

from fastapi import APIRouter

from api.responses import success_response
from api.services import analytics_api_service

router = APIRouter(prefix="/transfer", tags=["Transfer Intelligence"])


@router.get("")
def get_transfer() -> dict[str, object]:
    return success_response("Transfer intelligence retrieved successfully", analytics_api_service.transfer())


@router.get("/targets")
def get_transfer_targets() -> dict[str, object]:
    return success_response("Transfer targets retrieved successfully", analytics_api_service.transfer_targets())


@router.get("/value")
def get_transfer_value() -> dict[str, object]:
    return success_response("Transfer value analysis retrieved successfully", analytics_api_service.transfer_value())