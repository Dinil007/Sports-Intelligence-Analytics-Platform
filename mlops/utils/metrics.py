"""MLOps metrics calculation utilities."""

from __future__ import annotations

import numpy as np

def calculate_psi(baseline: list[float] | np.ndarray, target: list[float] | np.ndarray, bins: int = 10) -> float:
    """Calculate Population Stability Index (PSI) between baseline and target distributions."""
    baseline = np.array(baseline)
    target = np.array(target)
    
    if len(baseline) == 0 or len(target) == 0:
        return 0.0

    # Determine bin edges from baseline
    percentiles = np.linspace(0, 100, bins + 1)
    bin_edges = np.percentile(baseline, percentiles)
    
    # Adjust edges to handle duplicates
    bin_edges = np.unique(bin_edges)
    if len(bin_edges) < 2:
        return 0.0
        
    baseline_counts, _ = np.histogram(baseline, bins=bin_edges)
    target_counts, _ = np.histogram(target, bins=bin_edges)
    
    # Calculate proportions with small epsilon to avoid divide-by-zero
    epsilon = 0.0001
    baseline_props = (baseline_counts + epsilon) / (len(baseline) + epsilon * len(baseline_counts))
    target_props = (target_counts + epsilon) / (len(target) + epsilon * len(target_counts))
    
    # Calculate PSI
    psi = np.sum((target_props - baseline_props) * np.log(target_props / baseline_props))
    return float(psi)
