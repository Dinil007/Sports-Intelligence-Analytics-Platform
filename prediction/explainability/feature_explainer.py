"""Deterministic model explanation generators."""

from __future__ import annotations

import numpy as np
from typing import Any, Dict, List
from prediction.explainability.shap_analysis import calculate_shap_values

class FeatureExplainer:
    """Explains model decisions using Shapley values or fallback coefficient analysis."""
    
    @staticmethod
    def explain_instance(
        model: Any,
        instance: np.ndarray,
        feature_names: List[str],
    ) -> Dict[str, float]:
        """Explain predictions for a single instance (row).
        
        Returns:
            Dict mapping feature names to their contribution (direction and magnitude).
        """
        # Simple contribution estimation based on relative values or SHAP if available
        # In this implementation, we calculate baseline global importances and weigh by instance values
        contributions = {}
        global_shap = calculate_shap_values(model, np.atleast_2d(instance), feature_names)
        
        # Normalize instance features (simple z-score scale representation)
        flat_instance = instance.flatten()
        
        for name, weight in global_shap.items():
            if name in feature_names:
                idx = feature_names.index(name)
                # Compute contribution as weight multiplied by relative value direction
                val = float(flat_instance[idx])
                direction = 1.0 if val >= 0.0 else -1.0
                contributions[name] = float(weight * direction)
                
        return contributions
