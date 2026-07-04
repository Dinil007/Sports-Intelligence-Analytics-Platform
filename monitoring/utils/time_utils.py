"""Time utilities for monitoring platform."""
from __future__ import annotations

from datetime import datetime, timezone

def get_current_iso_timestamp() -> str:
    """Get current timestamp in ISO Format."""
    return datetime.now(timezone.utc).isoformat()

def format_iso_timestamp(timestamp: str) -> str:
    """Safely format an ISO timestamp for display."""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return timestamp
