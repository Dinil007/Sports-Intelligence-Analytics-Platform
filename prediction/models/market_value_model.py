"""Market Value estimation regression model."""

from __future__ import annotations

from typing import Any, List
from xgboost import XGBRegressor # type: ignore
from prediction.config import config

FEATURE_COLS: List[str] = [
    "age",
    "goals_per_season",
    "assists_per_season",
    "sporta_score",
    "international_caps",
    "league_level",
    "years_contract_remaining",
    "pass_completion_rate",
    "goals_per_90",
]

TARGET_COL = "market_value_eur"

def build_model() -> Any:
    """Return a configured XGBoost Regressor for market value estimation."""
    return XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=config.RANDOM_STATE,
    )
