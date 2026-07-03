"""Training pipeline for the Transfer Success prediction model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score # type: ignore
from prediction.models.transfer_success_model import build_model, FEATURE_COLS, TARGET_COL
from prediction.utils.preprocessing import DataPreprocessor
from prediction.utils.data_split import split_dataset
from prediction.utils.serialization import ModelSerializer
from prediction.evaluation.classification_metrics import evaluate_classification
from prediction.evaluation.model_report import ModelEvaluationReport
from prediction.registry.model_registry import ModelRegistry
from prediction.constants import MODEL_TRANSFER_SUCCESS
from prediction.config import config
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_TRANSFER_SUCCESS}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_TRANSFER_SUCCESS}_preprocessor.joblib"

def _generate_synthetic_data(n: int = 600) -> pd.DataFrame:
    rng = np.random.default_rng(config.RANDOM_STATE)
    df = pd.DataFrame({
        "player_age": rng.integers(16, 36, n).astype(float),
        "market_value": rng.uniform(0.5e6, 120e6, n),
        "goals_per_season": rng.uniform(0, 35, n),
        "assists_per_season": rng.uniform(0, 20, n),
        "minutes_played": rng.integers(500, 3400, n).astype(float),
        "league_level": rng.integers(1, 6, n).astype(float),
        "transfer_fee": rng.uniform(0.5e6, 150e6, n),
        "destination_league_level": rng.integers(1, 6, n).astype(float),
        "fitness_score": rng.uniform(60.0, 99.0, n),
    })
    df[TARGET_COL] = (
        (df["goals_per_season"] > 10)
        & (df["fitness_score"] > 75)
        & (df["player_age"] < 30)
    ).astype(int)
    return df

def train_transfer_model(df: pd.DataFrame | None = None) -> str:
    if df is None:
        logger.info("No data provided — using synthetic training data for transfer success model.")
        df = _generate_synthetic_data()

    X_train, X_test, y_train, y_test = split_dataset(df, TARGET_COL, stratify=True)
    preprocessor = DataPreprocessor(numeric_cols=FEATURE_COLS, categorical_cols=[])
    X_train_t = preprocessor.fit_transform(X_train[FEATURE_COLS])
    X_test_t = preprocessor.transform(X_test[FEATURE_COLS])

    model = build_model()
    cv_scores = cross_val_score(model, X_train_t, y_train.values, cv=5, scoring="f1")
    logger.info(f"Transfer Success Model — CV F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    model.fit(X_train_t, y_train.values)
    y_pred = model.predict(X_test_t)
    y_prob = model.predict_proba(X_test_t)
    metrics = evaluate_classification(y_test.values, y_pred, y_prob=y_prob)
    metrics["cv_f1"] = float(cv_scores.mean())

    report = ModelEvaluationReport.generate_report(MODEL_TRANSFER_SUCCESS, "LogisticRegression", metrics)
    logger.info(f"\n{report}")

    model_path = ModelSerializer.save(model, MODEL_FILENAME)
    ModelSerializer.save(preprocessor, PREPROCESSOR_FILENAME)

    return ModelRegistry.register_model(
        model_name=MODEL_TRANSFER_SUCCESS,
        algorithm="LogisticRegression",
        metrics=metrics,
        location=str(model_path),
        status="production",
    )
