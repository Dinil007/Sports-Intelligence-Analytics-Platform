"""Public inference API for all prediction models."""

from __future__ import annotations

from prediction.inference.predict_match import predict_match
from prediction.inference.predict_player_rating import predict_player_rating
from prediction.inference.predict_transfer_success import predict_transfer_success
from prediction.inference.predict_injury_risk import predict_injury_risk
from prediction.inference.predict_market_value import predict_market_value
from prediction.inference.predict_team_strength import predict_team_strength

__all__ = [
    "predict_match",
    "predict_player_rating",
    "predict_transfer_success",
    "predict_injury_risk",
    "predict_market_value",
    "predict_team_strength",
]
