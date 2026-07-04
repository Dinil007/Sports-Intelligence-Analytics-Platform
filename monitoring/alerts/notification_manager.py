"""Mock alert notifications dispatcher."""
from __future__ import annotations

from typing import Dict, Any

def dispatch_notification(alert: Dict[str, Any]) -> bool:
    """Mock alert notification dispatcher (always succeeds, no external calls)."""
    return True
