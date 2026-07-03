"""Team Strength Score prediction regression model."""

from __future__ import annotations

from typing import Any, List
from sklearn.ensemble import RandomForestRegressor # type: ignore
from prediction.config import config

FEATURE_COLS: List[str] = [
    "avg_player_rating",
    "goals_scored_season",
    "goals_conceded_season",
    "possession_avg",
    "pass_completion_avg",
    "xg_for",
    "xg_against",
    "win_rate",
    "clean_sheet_rate",
    "squad_depth_score",
]

TARGET_COL = "team_strength_score"

def build_model() -> Any:
    """Return a configured Random Forest Regressor for team strength estimation."""
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        random_state=config.RANDOM_STATE,
        n_jobs=-1,
    )
