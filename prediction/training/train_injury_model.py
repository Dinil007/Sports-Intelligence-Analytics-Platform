"""Training pipeline for the Injury Risk prediction model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score # type: ignore
from prediction.models.injury_risk_model import build_model, FEATURE_COLS, TARGET_COL
from prediction.utils.preprocessing import DataPreprocessor
from prediction.utils.data_split import split_dataset
from prediction.utils.serialization import ModelSerializer
from prediction.evaluation.classification_metrics import evaluate_classification
from prediction.evaluation.model_report import ModelEvaluationReport
from prediction.registry.model_registry import ModelRegistry
from prediction.constants import MODEL_INJURY_RISK
from prediction.config import config
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_INJURY_RISK}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_INJURY_RISK}_preprocessor.joblib"

def _generate_synthetic_data(n: int = 700) -> pd.DataFrame:
    rng = np.random.default_rng(config.RANDOM_STATE)
    df = pd.DataFrame({
        "age": rng.integers(16, 37, n).astype(float),
        "minutes_played_last_30": rng.integers(0, 720, n).astype(float),
        "fatigue_score": rng.uniform(20.0, 100.0, n),
        "sprint_count": rng.integers(10, 200, n).astype(float),
        "previous_injuries": rng.integers(0, 6, n).astype(float),
        "training_load": rng.uniform(30.0, 100.0, n),
        "bmi": rng.uniform(19.0, 28.0, n),
        "matches_last_30_days": rng.integers(0, 12, n).astype(float),
        "recovery_days": rng.integers(0, 7, n).astype(float),
    })
    # High risk when old, fatigued, many previous injuries
    risk = np.where(
        (df["fatigue_score"] > 80) & (df["previous_injuries"] >= 3), 2,
        np.where((df["fatigue_score"] > 60) | (df["previous_injuries"] >= 1), 1, 0)
    )
    df[TARGET_COL] = risk
    return df

def train_injury_model(df: pd.DataFrame | None = None) -> str:
    if df is None:
        logger.info("No data provided — using synthetic training data for injury risk model.")
        df = _generate_synthetic_data()

    X_train, X_test, y_train, y_test = split_dataset(df, TARGET_COL, stratify=True)
    preprocessor = DataPreprocessor(numeric_cols=FEATURE_COLS, categorical_cols=[])
    X_train_t = preprocessor.fit_transform(X_train[FEATURE_COLS])
    X_test_t = preprocessor.transform(X_test[FEATURE_COLS])

    model = build_model()
    cv_scores = cross_val_score(model, X_train_t, y_train.values, cv=5, scoring="accuracy")
    logger.info(f"Injury Risk Model — CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    model.fit(X_train_t, y_train.values)
    y_pred = model.predict(X_test_t)
    y_prob = model.predict_proba(X_test_t)
    metrics = evaluate_classification(y_test.values, y_pred, y_prob=y_prob)
    metrics["cv_accuracy"] = float(cv_scores.mean())

    report = ModelEvaluationReport.generate_report(MODEL_INJURY_RISK, "XGBClassifier", metrics)
    logger.info(f"\n{report}")

    model_path = ModelSerializer.save(model, MODEL_FILENAME)
    ModelSerializer.save(preprocessor, PREPROCESSOR_FILENAME)

    return ModelRegistry.register_model(
        model_name=MODEL_INJURY_RISK,
        algorithm="XGBClassifier",
        metrics=metrics,
        location=str(model_path),
        status="production",
    )
