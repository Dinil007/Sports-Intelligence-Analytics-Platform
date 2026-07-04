"""Platform audit log recorder."""
from __future__ import annotations

from typing import List, Dict, Any
from monitoring.audit.audit_events import get_simulated_audit_events

def log_audit_event(action: str, username: str, status: str, details: str = "") -> bool:
    """Mock record an audit event (always succeeds)."""
    return True

def fetch_audit_logs() -> List[Dict[str, Any]]:
    """Fetch recent system and user audit events."""
    return get_simulated_audit_events()
