"""Model definition schemas for all prediction tasks."""

from __future__ import annotations

from prediction.models.match_outcome_model import build_model as build_match_model
from prediction.models.player_rating_model import build_model as build_player_rating_model
from prediction.models.transfer_success_model import build_model as build_transfer_model
from prediction.models.injury_risk_model import build_model as build_injury_model
from prediction.models.market_value_model import build_model as build_market_value_model
from prediction.models.team_strength_model import build_model as build_team_strength_model

__all__ = [
    "build_match_model",
    "build_player_rating_model",
    "build_transfer_model",
    "build_injury_model",
    "build_market_value_model",
    "build_team_strength_model",
]
