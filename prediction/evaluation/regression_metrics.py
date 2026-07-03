"""Calculation of MAE, RMSE, and R2 metrics for regression models."""

from __future__ import annotations

import numpy as np
from typing import Dict, Union
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score # type: ignore

def evaluate_regression(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
) -> Dict[str, float]:
    """Calculate and return a dictionary of common regression metrics."""
    mse = float(mean_squared_error(y_true, y_pred))
    metrics = {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mse)),
        "r2_score": float(r2_score(y_true, y_pred)),
    }
    return metrics
