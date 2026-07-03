"""Transfer Success prediction model."""

from __future__ import annotations

from typing import Any, List
from sklearn.linear_model import LogisticRegression # type: ignore
from prediction.config import config

FEATURE_COLS: List[str] = [
    "player_age",
    "market_value",
    "goals_per_season",
    "assists_per_season",
    "minutes_played",
    "league_level",
    "transfer_fee",
    "destination_league_level",
    "fitness_score",
]

TARGET_COL = "transfer_success"  # 0=Unsuccessful, 1=Successful

def build_model() -> Any:
    """Return a configured Logistic Regression model for transfer success prediction."""
    return LogisticRegression(
        C=1.0,
        max_iter=500,
        solver="lbfgs",
        random_state=config.RANDOM_STATE,
    )
