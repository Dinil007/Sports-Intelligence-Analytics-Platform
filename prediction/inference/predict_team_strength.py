"""Inference endpoint for Team Strength Score estimation."""

from __future__ import annotations

from typing import Any, Dict
from prediction.constants import MODEL_TEAM_STRENGTH
from prediction.utils.serialization import ModelSerializer
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_TEAM_STRENGTH}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_TEAM_STRENGTH}_preprocessor.joblib"

def predict_team_strength(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict the overall strength score for a team.
    
    Returns:
        Dict with 'team_strength_score' (0–100 scale).
    """
    import pandas as pd
    try:
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)
    except FileNotFoundError:
        logger.warning("Team strength model not found. Training now...")
        from prediction.training.train_team_strength_model import train_team_strength_model
        train_team_strength_model()
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)

    df = pd.DataFrame([features])
    X = preprocessor.transform(df)
    score = float(model.predict(X)[0])
    score = round(max(10.0, min(100.0, score)), 2)

    result = {"team_strength_score": score}
    logger.info(f"Team strength prediction: {score}/100")
    return result
