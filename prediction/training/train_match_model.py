"""Training pipeline for the Match Outcome prediction model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score # type: ignore
from prediction.models.match_outcome_model import build_model, FEATURE_COLS, TARGET_COL
from prediction.utils.preprocessing import DataPreprocessor
from prediction.utils.data_split import split_dataset
from prediction.utils.serialization import ModelSerializer
from prediction.evaluation.classification_metrics import evaluate_classification
from prediction.evaluation.feature_importance import get_feature_importance
from prediction.evaluation.model_report import ModelEvaluationReport
from prediction.registry.model_registry import ModelRegistry
from prediction.constants import MODEL_MATCH_OUTCOME
from prediction.config import config
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_MATCH_OUTCOME}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_MATCH_OUTCOME}_preprocessor.joblib"

def _generate_synthetic_data(n: int = 800) -> pd.DataFrame:
    """Generate synthetic training data for the match outcome model."""
    rng = np.random.default_rng(config.RANDOM_STATE)
    df = pd.DataFrame({
        "home_goals_avg": rng.uniform(0.8, 2.8, n),
        "away_goals_avg": rng.uniform(0.8, 2.5, n),
        "home_shots_avg": rng.uniform(8.0, 18.0, n),
        "away_shots_avg": rng.uniform(6.0, 15.0, n),
        "home_possession_avg": rng.uniform(40.0, 65.0, n),
        "away_possession_avg": rng.uniform(35.0, 60.0, n),
        "home_win_rate": rng.uniform(0.2, 0.8, n),
        "away_win_rate": rng.uniform(0.2, 0.75, n),
        "goal_difference": rng.integers(-4, 5, n).astype(float),
    })
    # Derive outcome from home advantage + goal_difference
    outcome = np.where(
        df["goal_difference"] > 0.5, 2,
        np.where(df["goal_difference"] < -0.5, 0, 1)
    )
    df[TARGET_COL] = outcome
    return df

def train_match_model(df: pd.DataFrame | None = None) -> str:
    """Train the Match Outcome model and register it.
    
    Args:
        df: Optional training DataFrame. Uses synthetic data if None.
        
    Returns:
        Registered version string.
    """
    if df is None:
        logger.info("No data provided — using synthetic training data for match outcome model.")
        df = _generate_synthetic_data()

    X_train, X_test, y_train, y_test = split_dataset(df, TARGET_COL, stratify=True)

    preprocessor = DataPreprocessor(numeric_cols=FEATURE_COLS, categorical_cols=[])
    X_train_t = preprocessor.fit_transform(X_train[FEATURE_COLS])
    X_test_t = preprocessor.transform(X_test[FEATURE_COLS])

    model = build_model()
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_t, y_train.values, cv=5, scoring="accuracy")
    logger.info(f"Match Outcome Model — CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    model.fit(X_train_t, y_train.values)

    y_pred = model.predict(X_test_t)
    y_prob = model.predict_proba(X_test_t)
    metrics = evaluate_classification(y_test.values, y_pred, y_prob=y_prob)
    metrics["cv_accuracy"] = float(cv_scores.mean())

    feature_names = preprocessor.get_feature_names()
    report = ModelEvaluationReport.generate_report(MODEL_MATCH_OUTCOME, "GradientBoostingClassifier", metrics)
    logger.info(f"\n{report}")

    model_path = ModelSerializer.save(model, MODEL_FILENAME)
    ModelSerializer.save(preprocessor, PREPROCESSOR_FILENAME)

    version = ModelRegistry.register_model(
        model_name=MODEL_MATCH_OUTCOME,
        algorithm="GradientBoostingClassifier",
        metrics=metrics,
        location=str(model_path),
        status="production",
    )
    return version
