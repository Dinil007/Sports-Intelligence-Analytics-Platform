"""Health calculation utilities."""
from __future__ import annotations

from typing import Union
from monitoring.constants import STATUS_HEALTHY, STATUS_WARNING, STATUS_DEGRADED, STATUS_CRITICAL

def threshold_status(value: Union[int, float], warning_th: Union[int, float], critical_th: Union[int, float], reverse: bool = False) -> str:
    """Determine status based on warning and critical thresholds."""
    if not reverse:
        if value >= critical_th:
            return STATUS_CRITICAL
        if value >= warning_th:
            return STATUS_WARNING
        return STATUS_HEALTHY
    else:
        if value <= critical_th:
            return STATUS_CRITICAL
        if value <= warning_th:
            return STATUS_WARNING
        return STATUS_HEALTHY
