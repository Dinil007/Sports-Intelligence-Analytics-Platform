"""Alert manager lifecycle."""
from __future__ import annotations

from typing import List, Dict, Any
from monitoring.alerts.alert_engine import run_alert_rules

def get_active_alerts() -> List[Dict[str, Any]]:
    """Return all active alerts currently raised."""
    return run_alert_rules()
