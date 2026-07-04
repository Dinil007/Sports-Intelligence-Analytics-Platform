"""Security audit and alert monitoring."""
from __future__ import annotations

from typing import List, Dict, Any

def get_security_events() -> List[Dict[str, Any]]:
    """Return security log highlights."""
    return [
        {"event": "User admin password change", "status": "Success", "occurred_at": "2026-07-04T08:00:00Z"},
        {"event": "Failed login attempt: root", "status": "Blocked", "occurred_at": "2026-07-04T10:12:00Z"},
    ]
