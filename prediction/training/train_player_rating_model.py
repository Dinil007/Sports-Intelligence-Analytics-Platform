"""Training pipeline for the Player Rating prediction model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score # type: ignore
from prediction.models.player_rating_model import build_model, FEATURE_COLS, TARGET_COL
from prediction.utils.preprocessing import DataPreprocessor
from prediction.utils.data_split import split_dataset
from prediction.utils.serialization import ModelSerializer
from prediction.evaluation.regression_metrics import evaluate_regression
from prediction.evaluation.model_report import ModelEvaluationReport
from prediction.registry.model_registry import ModelRegistry
from prediction.constants import MODEL_PLAYER_RATING
from prediction.config import config
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_PLAYER_RATING}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_PLAYER_RATING}_preprocessor.joblib"

def _generate_synthetic_data(n: int = 800) -> pd.DataFrame:
    rng = np.random.default_rng(config.RANDOM_STATE)
    df = pd.DataFrame({
        "goals": rng.integers(0, 5, n).astype(float),
        "assists": rng.integers(0, 4, n).astype(float),
        "passes_completed": rng.uniform(20.0, 90.0, n),
        "pass_completion_rate": rng.uniform(0.55, 0.98, n),
        "shots_on_target": rng.integers(0, 6, n).astype(float),
        "tackles_won": rng.integers(0, 8, n).astype(float),
        "interceptions": rng.integers(0, 5, n).astype(float),
        "key_passes": rng.integers(0, 6, n).astype(float),
        "dribbles_completed": rng.integers(0, 7, n).astype(float),
        "minutes_played": rng.integers(45, 90, n).astype(float),
    })
    df[TARGET_COL] = (
        6.5
        + df["goals"] * 0.6
        + df["assists"] * 0.4
        + df["key_passes"] * 0.15
        + df["pass_completion_rate"] * 0.5
        + rng.normal(0, 0.3, n)
    ).clip(5.0, 10.0)
    return df

def train_player_rating_model(df: pd.DataFrame | None = None) -> str:
    if df is None:
        logger.info("No data provided — using synthetic training data for player rating model.")
        df = _generate_synthetic_data()

    X_train, X_test, y_train, y_test = split_dataset(df, TARGET_COL)

    preprocessor = DataPreprocessor(numeric_cols=FEATURE_COLS, categorical_cols=[])
    X_train_t = preprocessor.fit_transform(X_train[FEATURE_COLS])
    X_test_t = preprocessor.transform(X_test[FEATURE_COLS])

    model = build_model()
    cv_scores = cross_val_score(model, X_train_t, y_train.values, cv=5, scoring="r2")
    logger.info(f"Player Rating Model — CV R2: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    model.fit(X_train_t, y_train.values)
    y_pred = model.predict(X_test_t)
    metrics = evaluate_regression(y_test.values, y_pred)
    metrics["cv_r2"] = float(cv_scores.mean())

    report = ModelEvaluationReport.generate_report(MODEL_PLAYER_RATING, "RandomForestRegressor", metrics, classification=False)
    logger.info(f"\n{report}")

    model_path = ModelSerializer.save(model, MODEL_FILENAME)
    ModelSerializer.save(preprocessor, PREPROCESSOR_FILENAME)

    return ModelRegistry.register_model(
        model_name=MODEL_PLAYER_RATING,
        algorithm="RandomForestRegressor",
        metrics=metrics,
        location=str(model_path),
        status="production",
    )
