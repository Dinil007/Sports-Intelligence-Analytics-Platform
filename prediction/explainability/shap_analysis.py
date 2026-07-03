"""SHAP (Shapley Additive exPlanations) fallback-aware wrapper."""

from __future__ import annotations

import numpy as np
from typing import Any, Dict, List
from prediction.logging import logger

def calculate_shap_values(model: Any, X: np.ndarray, feature_names: List[str]) -> Dict[str, float]:
    """Calculate average absolute SHAP values for each feature.
    
    If shap package is not available, falls back to feature importance scores.
    """
    try:
        import shap # type: ignore
        logger.info("Using real shap package for explainability.")
        
        # Determine suitable explainer
        if hasattr(model, "feature_importances_"):
            explainer = shap.TreeExplainer(model)
        else:
            explainer = shap.Explainer(model, X)
            
        shap_values = explainer(X)
        
        # Handle multi-class outputs or standard outputs
        if len(shap_values.shape) > 2:
            # Multi-class output: shape (samples, features, classes)
            mean_abs_shap = np.mean(np.abs(shap_values.values), axis=(0, 2))
        else:
            mean_abs_shap = np.mean(np.abs(shap_values.values), axis=0)
            
        result = {}
        for name, val in zip(feature_names, mean_abs_shap):
            result[name] = float(val)
            
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        
    except Exception as e:
        logger.warning(f"SHAP package not available or failed: {e}. Falling back to deterministic feature importance scores.")
        from prediction.evaluation.feature_importance import get_feature_importance
        return get_feature_importance(model, feature_names)
