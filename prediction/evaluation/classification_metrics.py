"""Calculation of accuracy, precision, recall, F1-score, and ROC AUC for classifiers."""

from __future__ import annotations

import numpy as np
from typing import Dict, Optional, Union
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score # type: ignore

def evaluate_classification(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
    y_prob: Optional[Union[np.ndarray, list]] = None,
    average: str = "weighted",
) -> Dict[str, float]:
    """Calculate and return a dictionary of common classification metrics."""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
    }
    
    if y_prob is not None:
        try:
            # Handle multi-class vs binary ROC AUC
            if len(np.unique(y_true)) > 2:
                metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob, multi_class="ovr", average=average))
            else:
                # If y_prob has 2 columns, select the positive class probabilities
                if isinstance(y_prob, np.ndarray) and len(y_prob.shape) == 2 and y_prob.shape[1] == 2:
                    y_prob_positive = y_prob[:, 1]
                else:
                    y_prob_positive = y_prob
                metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob_positive))
        except Exception:
            metrics["roc_auc"] = 0.0
            
    return metrics
