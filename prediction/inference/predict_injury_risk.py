"""Inference endpoint for Injury Risk prediction."""

from __future__ import annotations

from typing import Any, Dict
from prediction.constants import MODEL_INJURY_RISK
from prediction.models.injury_risk_model import LABEL_MAP
from prediction.utils.serialization import ModelSerializer
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_INJURY_RISK}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_INJURY_RISK}_preprocessor.joblib"

def predict_injury_risk(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict the injury risk level for a player.
    
    Returns:
        Dict with 'risk_level' (Low/Medium/High) and 'probability'.
    """
    import pandas as pd
    try:
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)
    except FileNotFoundError:
        logger.warning("Injury risk model not found. Training now...")
        from prediction.training.train_injury_model import train_injury_model
        train_injury_model()
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)

    df = pd.DataFrame([features])
    X = preprocessor.transform(df)
    pred_class = int(model.predict(X)[0])
    pred_probs = model.predict_proba(X)[0]

    result = {
        "risk_level": LABEL_MAP.get(pred_class, str(pred_class)),
        "confidence": float(max(pred_probs)),
        "probabilities": {LABEL_MAP.get(i, str(i)): float(p) for i, p in enumerate(pred_probs)},
    }
    logger.info(f"Injury risk prediction: {result['risk_level']} ({result['confidence']:.2%})")
    return result
