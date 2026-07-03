"""Standard evaluation functions for accuracy, precision, MAE, R2, and reports."""

from __future__ import annotations

from prediction.evaluation.classification_metrics import evaluate_classification
from prediction.evaluation.regression_metrics import evaluate_regression
from prediction.evaluation.confusion_matrix import get_confusion_matrix
from prediction.evaluation.feature_importance import get_feature_importance
from prediction.evaluation.model_report import ModelEvaluationReport

__all__ = [
    "evaluate_classification",
    "evaluate_regression",
    "get_confusion_matrix",
    "get_feature_importance",
    "ModelEvaluationReport",
]
