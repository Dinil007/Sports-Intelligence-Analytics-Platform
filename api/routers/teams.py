from __future__ import annotations

from fastapi import APIRouter, Depends

from api.dependencies import LimitQuery, pagination_params
from api.responses import success_response
from api.services import team_api_service
from api.utils.pagination import PaginationParams
from api.utils.validators import validate_positive_id

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("")
def get_teams(params: PaginationParams = Depends(pagination_params)) -> dict[str, object]:
    return success_response("Teams retrieved successfully", team_api_service.list_teams(params.page, params.page_size))


@router.get("/rankings")
def get_team_rankings(limit: LimitQuery = 25) -> dict[str, object]:
    return success_response("Team rankings retrieved successfully", team_api_service.team_rankings(limit))


@router.get("/{team_id}")
def get_team(team_id: int) -> dict[str, object]:
    return success_response("Team retrieved successfully", team_api_service.get_team(validate_positive_id(team_id, "team_id")))