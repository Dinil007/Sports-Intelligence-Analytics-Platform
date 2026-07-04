"""Alert rule definitions and thresholds."""
from __future__ import annotations

from typing import Dict, Any

# Alert Threshold configs
CPU_WARNING_THRESHOLD = 80.0
CPU_CRITICAL_THRESHOLD = 90.0

MEM_WARNING_THRESHOLD = 85.0
MEM_CRITICAL_THRESHOLD = 95.0

DB_CONN_WARNING_THRESHOLD = 80.0
DB_CONN_CRITICAL_THRESHOLD = 95.0

def get_alert_thresholds() -> Dict[str, Any]:
    """Get active config thresholds."""
    return {
        "cpu_warning": CPU_WARNING_THRESHOLD,
        "cpu_critical": CPU_CRITICAL_THRESHOLD,
        "mem_warning": MEM_WARNING_THRESHOLD,
        "mem_critical": MEM_CRITICAL_THRESHOLD,
        "db_conn_warning": DB_CONN_WARNING_THRESHOLD,
        "db_conn_critical": DB_CONN_CRITICAL_THRESHOLD,
    }
