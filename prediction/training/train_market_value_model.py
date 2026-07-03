"""Training pipeline for the Market Value estimation model."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score # type: ignore
from prediction.models.market_value_model import build_model, FEATURE_COLS, TARGET_COL
from prediction.utils.preprocessing import DataPreprocessor
from prediction.utils.data_split import split_dataset
from prediction.utils.serialization import ModelSerializer
from prediction.evaluation.regression_metrics import evaluate_regression
from prediction.evaluation.model_report import ModelEvaluationReport
from prediction.registry.model_registry import ModelRegistry
from prediction.constants import MODEL_MARKET_VALUE
from prediction.config import config
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_MARKET_VALUE}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_MARKET_VALUE}_preprocessor.joblib"

def _generate_synthetic_data(n: int = 800) -> pd.DataFrame:
    rng = np.random.default_rng(config.RANDOM_STATE)
    df = pd.DataFrame({
        "age": rng.integers(16, 36, n).astype(float),
        "goals_per_season": rng.uniform(0, 35, n),
        "assists_per_season": rng.uniform(0, 20, n),
        "sporta_score": rng.uniform(50.0, 99.0, n),
        "international_caps": rng.integers(0, 100, n).astype(float),
        "league_level": rng.integers(1, 6, n).astype(float),
        "years_contract_remaining": rng.uniform(0, 5, n),
        "pass_completion_rate": rng.uniform(0.55, 0.98, n),
        "goals_per_90": rng.uniform(0, 1.2, n),
    })
    df[TARGET_COL] = (
        (df["sporta_score"] * 0.6
         + df["goals_per_season"] * 2.5
         + df["assists_per_season"] * 1.5
         + df["international_caps"] * 0.4
         + rng.normal(0, 5, n))
        * 1e6
    ).clip(100_000, 200_000_000)
    return df

def train_market_value_model(df: pd.DataFrame | None = None) -> str:
    if df is None:
        logger.info("No data provided — using synthetic training data for market value model.")
        df = _generate_synthetic_data()

    X_train, X_test, y_train, y_test = split_dataset(df, TARGET_COL)
    preprocessor = DataPreprocessor(numeric_cols=FEATURE_COLS, categorical_cols=[])
    X_train_t = preprocessor.fit_transform(X_train[FEATURE_COLS])
    X_test_t = preprocessor.transform(X_test[FEATURE_COLS])

    model = build_model()
    cv_scores = cross_val_score(model, X_train_t, y_train.values, cv=5, scoring="r2")
    logger.info(f"Market Value Model — CV R2: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    model.fit(X_train_t, y_train.values)
    y_pred = model.predict(X_test_t)
    metrics = evaluate_regression(y_test.values, y_pred)
    metrics["cv_r2"] = float(cv_scores.mean())

    report = ModelEvaluationReport.generate_report(MODEL_MARKET_VALUE, "XGBRegressor", metrics, classification=False)
    logger.info(f"\n{report}")

    model_path = ModelSerializer.save(model, MODEL_FILENAME)
    ModelSerializer.save(preprocessor, PREPROCESSOR_FILENAME)

    return ModelRegistry.register_model(
        model_name=MODEL_MARKET_VALUE,
        algorithm="XGBRegressor",
        metrics=metrics,
        location=str(model_path),
        status="production",
    )
