"""Calculates statistical metrics for Observability platform."""
from __future__ import annotations

from typing import List, Union

def calculate_average(values: List[Union[int, float]]) -> float:
    """Calculate average value."""
    if not values:
        return 0.0
    return sum(values) / len(values)

def calculate_p95(values: List[Union[int, float]]) -> float:
    """Calculate 95th percentile value."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * 0.95)
    return float(sorted_vals[min(idx, len(sorted_vals) - 1)])
