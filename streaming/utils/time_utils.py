"""Time and timezone utility functions for event processing."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Union

def get_utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)

def format_iso_timestamp(dt: datetime) -> str:
    """Format a datetime to standard UTC ISO-8601 string."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

def parse_timestamp(ts: Union[str, datetime, float]) -> datetime:
    """Safely parse various formats into a timezone-aware UTC datetime."""
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            return ts.replace(tzinfo=timezone.utc)
        return ts
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, timezone.utc)
    
    # Try parsing string
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        # Fallback to current UTC
        return get_utc_now()
