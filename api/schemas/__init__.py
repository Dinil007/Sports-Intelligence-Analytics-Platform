"""Pydantic schemas for the SPORTA VISTA PRO API."""

from api.schemas.analytics import AnalyticsResponse
from api.schemas.athlete import AthleteResponse
from api.schemas.common import ErrorResponse, PaginatedData, PaginationResponse, SuccessResponse
from api.schemas.injury import InjuryResponse
from api.schemas.match import MatchResponse
from api.schemas.player import PlayerResponse
from api.schemas.scouting import ScoutingResponse
from api.schemas.team import TeamResponse
from api.schemas.transfer import TransferResponse

__all__ = [
    "AnalyticsResponse",
    "AthleteResponse",
    "ErrorResponse",
    "InjuryResponse",
    "MatchResponse",
    "PaginatedData",
    "PaginationResponse",
    "PlayerResponse",
    "ScoutingResponse",
    "SuccessResponse",
    "TeamResponse",
    "TransferResponse",
]