"""Inference endpoint for Player Market Value estimation."""

from __future__ import annotations

from typing import Any, Dict
from prediction.constants import MODEL_MARKET_VALUE
from prediction.utils.serialization import ModelSerializer
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_MARKET_VALUE}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_MARKET_VALUE}_preprocessor.joblib"

def predict_market_value(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict the estimated market value (EUR) for a player.
    
    Returns:
        Dict with 'estimated_value_eur' float.
    """
    import pandas as pd
    try:
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)
    except FileNotFoundError:
        logger.warning("Market value model not found. Training now...")
        from prediction.training.train_market_value_model import train_market_value_model
        train_market_value_model()
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)

    df = pd.DataFrame([features])
    X = preprocessor.transform(df)
    value = float(model.predict(X)[0])
    value = max(100_000.0, value)

    result = {
        "estimated_value_eur": round(value, 2),
        "estimated_value_m": round(value / 1_000_000, 2),
    }
    logger.info(f"Market value prediction: €{result['estimated_value_m']}M")
    return result
