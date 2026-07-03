"""Inference endpoint for Match Outcome prediction."""

from __future__ import annotations

from typing import Any, Dict
from prediction.constants import MODEL_MATCH_OUTCOME
from prediction.models.match_outcome_model import LABEL_MAP
from prediction.utils.serialization import ModelSerializer
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_MATCH_OUTCOME}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_MATCH_OUTCOME}_preprocessor.joblib"

def predict_match(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict the outcome of a football match.
    
    Args:
        features: Dict with keys matching match_outcome_model.FEATURE_COLS.
        
    Returns:
        Dict with 'prediction' label and 'probabilities' dict.
    """
    import pandas as pd
    try:
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)
    except FileNotFoundError:
        logger.warning("Match outcome model not found. Training now with synthetic data...")
        from prediction.training.train_match_model import train_match_model
        train_match_model()
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)

    df = pd.DataFrame([features])
    X = preprocessor.transform(df)
    pred_class = int(model.predict(X)[0])
    pred_probs = model.predict_proba(X)[0]

    result = {
        "prediction": LABEL_MAP.get(pred_class, str(pred_class)),
        "confidence": float(max(pred_probs)),
        "probabilities": {LABEL_MAP.get(i, str(i)): float(p) for i, p in enumerate(pred_probs)},
    }
    logger.info(f"Match outcome prediction: {result['prediction']} ({result['confidence']:.2%})")
    return result
