"""Training pipeline for the Team Strength Score model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score # type: ignore
from prediction.models.team_strength_model import build_model, FEATURE_COLS, TARGET_COL
from prediction.utils.preprocessing import DataPreprocessor
from prediction.utils.data_split import split_dataset
from prediction.utils.serialization import ModelSerializer
from prediction.evaluation.regression_metrics import evaluate_regression
from prediction.evaluation.model_report import ModelEvaluationReport
from prediction.registry.model_registry import ModelRegistry
from prediction.constants import MODEL_TEAM_STRENGTH
from prediction.config import config
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_TEAM_STRENGTH}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_TEAM_STRENGTH}_preprocessor.joblib"

def _generate_synthetic_data(n: int = 500) -> pd.DataFrame:
    rng = np.random.default_rng(config.RANDOM_STATE)
    df = pd.DataFrame({
        "avg_player_rating": rng.uniform(5.5, 9.0, n),
        "goals_scored_season": rng.integers(20, 100, n).astype(float),
        "goals_conceded_season": rng.integers(15, 80, n).astype(float),
        "possession_avg": rng.uniform(38.0, 65.0, n),
        "pass_completion_avg": rng.uniform(0.6, 0.95, n),
        "xg_for": rng.uniform(0.5, 3.0, n),
        "xg_against": rng.uniform(0.5, 2.5, n),
        "win_rate": rng.uniform(0.1, 0.85, n),
        "clean_sheet_rate": rng.uniform(0.05, 0.6, n),
        "squad_depth_score": rng.uniform(40.0, 100.0, n),
    })
    df[TARGET_COL] = (
        df["avg_player_rating"] * 8
        + df["win_rate"] * 30
        + df["clean_sheet_rate"] * 15
        + df["squad_depth_score"] * 0.3
        + rng.normal(0, 2, n)
    ).clip(10.0, 100.0)
    return df

def train_team_strength_model(df: pd.DataFrame | None = None) -> str:
    if df is None:
        logger.info("No data provided — using synthetic training data for team strength model.")
        df = _generate_synthetic_data()

    X_train, X_test, y_train, y_test = split_dataset(df, TARGET_COL)
    preprocessor = DataPreprocessor(numeric_cols=FEATURE_COLS, categorical_cols=[])
    X_train_t = preprocessor.fit_transform(X_train[FEATURE_COLS])
    X_test_t = preprocessor.transform(X_test[FEATURE_COLS])

    model = build_model()
    cv_scores = cross_val_score(model, X_train_t, y_train.values, cv=5, scoring="r2")
    logger.info(f"Team Strength Model — CV R2: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    model.fit(X_train_t, y_train.values)
    y_pred = model.predict(X_test_t)
    metrics = evaluate_regression(y_test.values, y_pred)
    metrics["cv_r2"] = float(cv_scores.mean())

    report = ModelEvaluationReport.generate_report(MODEL_TEAM_STRENGTH, "RandomForestRegressor", metrics, classification=False)
    logger.info(f"\n{report}")

    model_path = ModelSerializer.save(model, MODEL_FILENAME)
    ModelSerializer.save(preprocessor, PREPROCESSOR_FILENAME)

    return ModelRegistry.register_model(
        model_name=MODEL_TEAM_STRENGTH,
        algorithm="RandomForestRegressor",
        metrics=metrics,
        location=str(model_path),
        status="production",
    )
