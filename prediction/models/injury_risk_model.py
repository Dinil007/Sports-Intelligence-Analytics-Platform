"""Injury Risk prediction model (Low / Medium / High)."""

from __future__ import annotations

from typing import Any, List
from xgboost import XGBClassifier # type: ignore
from prediction.config import config

FEATURE_COLS: List[str] = [
    "age",
    "minutes_played_last_30",
    "fatigue_score",
    "sprint_count",
    "previous_injuries",
    "training_load",
    "bmi",
    "matches_last_30_days",
    "recovery_days",
]

TARGET_COL = "injury_risk"  # 0=Low, 1=Medium, 2=High
LABEL_MAP = {0: "Low", 1: "Medium", 2: "High"}

def build_model() -> Any:
    """Return a configured XGBoost Classifier for injury risk prediction."""
    return XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=config.RANDOM_STATE,
        eval_metric="mlogloss",
        use_label_encoder=False,
    )
