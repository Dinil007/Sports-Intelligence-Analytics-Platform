"""Player Match Rating prediction model."""

from __future__ import annotations

from typing import Any, List
from sklearn.ensemble import RandomForestRegressor # type: ignore
from prediction.config import config

FEATURE_COLS: List[str] = [
    "goals",
    "assists",
    "passes_completed",
    "pass_completion_rate",
    "shots_on_target",
    "tackles_won",
    "interceptions",
    "key_passes",
    "dribbles_completed",
    "minutes_played",
]

TARGET_COL = "match_rating"

def build_model() -> Any:
    """Return a configured Random Forest Regressor for player rating prediction."""
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_split=4,
        random_state=config.RANDOM_STATE,
        n_jobs=-1,
    )
