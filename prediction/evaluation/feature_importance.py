"""Extraction and sorting of model feature importances."""

from __future__ import annotations

import numpy as np
from typing import Any, Dict, List

def get_feature_importance(model: Any, feature_names: List[str]) -> Dict[str, float]:
    """Extract and sort feature importance coefficients or importances from a trained model."""
    importances = {}
    
    # 1. Check feature_importances_ (Trees/Ensembles/XGBoost)
    if hasattr(model, "feature_importances_"):
        raw_importances = model.feature_importances_
        for name, val in zip(feature_names, raw_importances):
            importances[name] = float(val)
            
    # 2. Check coef_ (Linear models)
    elif hasattr(model, "coef_"):
        raw_coefs = model.coef_
        # If multi-class coefficients, take average of absolute values
        if len(raw_coefs.shape) > 1:
            raw_coefs = np.mean(np.abs(raw_coefs), axis=0)
        else:
            raw_coefs = np.abs(raw_coefs)
            
        for name, val in zip(feature_names, raw_coefs):
            importances[name] = float(val)
            
    # 3. Fallback equal importances
    else:
        for name in feature_names:
            importances[name] = 1.0 / max(1, len(feature_names))

    # Sort descending
    sorted_importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))
    return sorted_importances
