"""Constants for prediction models and task names."""

from __future__ import annotations

# Model Names
MODEL_MATCH_OUTCOME = "match_outcome_model"
MODEL_PLAYER_RATING = "player_rating_model"
MODEL_TRANSFER_SUCCESS = "transfer_success_model"
MODEL_INJURY_RISK = "injury_risk_model"
MODEL_MARKET_VALUE = "market_value_model"
MODEL_TEAM_STRENGTH = "team_strength_model"

ALL_MODELS = (
    MODEL_MATCH_OUTCOME,
    MODEL_PLAYER_RATING,
    MODEL_TRANSFER_SUCCESS,
    MODEL_INJURY_RISK,
    MODEL_MARKET_VALUE,
    MODEL_TEAM_STRENGTH,
)

# Registry configurations
REGISTRY_FILENAME = "registry.json"
MODELS_DIR_NAME = "serialized_models"
