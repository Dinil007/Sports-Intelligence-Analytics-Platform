from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from api.dependencies import LimitQuery, pagination_params
from api.responses import success_response
from api.services import player_api_service
from api.utils.pagination import PaginationParams
from api.utils.validators import validate_positive_id

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("")
def get_players(params: PaginationParams = Depends(pagination_params)) -> dict[str, object]:
    return success_response("Players retrieved successfully", player_api_service.list_players(params.page, params.page_size))


@router.get("/search")
def search_players(q: str | None = Query(None, min_length=1), limit: LimitQuery = 25) -> dict[str, object]:
    return success_response("Players search completed successfully", player_api_service.search_players(q, limit))


@router.get("/top")
def top_players(limit: LimitQuery = 25) -> dict[str, object]:
    return success_response("Top players retrieved successfully", player_api_service.top_players(limit))


@router.get("/{player_id}")
def get_player(player_id: int) -> dict[str, object]:
    return success_response("Player retrieved successfully", player_api_service.get_player(validate_positive_id(player_id, "player_id")))