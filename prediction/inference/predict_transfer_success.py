"""Inference endpoint for Transfer Success prediction."""

from __future__ import annotations

from typing import Any, Dict
from prediction.constants import MODEL_TRANSFER_SUCCESS
from prediction.utils.serialization import ModelSerializer
from prediction.logging import logger

MODEL_FILENAME = f"{MODEL_TRANSFER_SUCCESS}.joblib"
PREPROCESSOR_FILENAME = f"{MODEL_TRANSFER_SUCCESS}_preprocessor.joblib"

def predict_transfer_success(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict whether a transfer is likely to be successful.
    
    Returns:
        Dict with 'prediction' (Successful/Unsuccessful), 'probability' float.
    """
    import pandas as pd
    try:
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)
    except FileNotFoundError:
        logger.warning("Transfer success model not found. Training now...")
        from prediction.training.train_transfer_model import train_transfer_model
        train_transfer_model()
        preprocessor = ModelSerializer.load(PREPROCESSOR_FILENAME)
        model = ModelSerializer.load(MODEL_FILENAME)

    df = pd.DataFrame([features])
    X = preprocessor.transform(df)
    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][pred])

    result = {
        "prediction": "Successful" if pred == 1 else "Unsuccessful",
        "probability": round(prob, 4),
    }
    logger.info(f"Transfer success prediction: {result['prediction']} ({prob:.2%})")
    return result
