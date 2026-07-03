"""Match Outcome prediction model (Home Win / Draw / Away Win)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional
from sklearn.ensemble import GradientBoostingClassifier # type: ignore
from prediction.config import config

# Feature columns this model expects
FEATURE_COLS: List[str] = [
    "home_goals_avg",
    "away_goals_avg",
    "home_shots_avg",
    "away_shots_avg",
    "home_possession_avg",
    "away_possession_avg",
    "home_win_rate",
    "away_win_rate",
    "goal_difference",
]

TARGET_COL = "outcome"  # 0=AwayWin, 1=Draw, 2=HomeWin
LABEL_MAP = {0: "Away Win", 1: "Draw", 2: "Home Win"}

def build_model() -> Any:
    """Return a configured Gradient Boosting Classifier for match outcome prediction."""
    return GradientBoostingClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.85,
        random_state=config.RANDOM_STATE,
    )
