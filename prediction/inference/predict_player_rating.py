"""Inference endpoint for Player Rating prediction."""

from __future__ import annotations

from typing import Any, Dict
from prediction.constants import MODEL_PLAYER_RATING
from prediction.utils.serialization import ModelSerializer
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_PLAYER_RATING}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_PLAYER_RATING}_preprocessor.joblib"

def predict_player_rating(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict the match rating for a player.
    
    Args:
        features: Dict with keys matching player_rating_model.FEATURE_COLS.
        
    Returns:
        Dict with 'predicted_rating' (float, 5.0–10.0).
    """
    import pandas as pd
    try:
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)
    except FileNotFoundError:
        logger.warning("Player rating model not found. Training now...")
        from prediction.training.train_player_rating_model import train_player_rating_model
        train_player_rating_model()
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)

    df = pd.DataFrame([features])
    X = preprocessor.transform(df)
    rating = float(model.predict(X)[0])
    rating = round(max(5.0, min(10.0, rating)), 2)

    result = {"predicted_rating": rating}
    logger.info(f"Player rating prediction: {rating}")
    return result
