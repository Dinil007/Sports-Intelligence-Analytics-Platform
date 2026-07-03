"""All model training pipelines."""

from __future__ import annotations

from prediction.training.train_match_model import train_match_model
from prediction.training.train_player_rating_model import train_player_rating_model
from prediction.training.train_transfer_model import train_transfer_model
from prediction.training.train_injury_model import train_injury_model
from prediction.training.train_market_value_model import train_market_value_model
from prediction.training.train_team_strength_model import train_team_strength_model

__all__ = [
    "train_match_model",
    "train_player_rating_model",
    "train_transfer_model",
    "train_injury_model",
    "train_market_value_model",
    "train_team_strength_model",
]
