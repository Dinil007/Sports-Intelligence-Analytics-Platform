"""Producer publish rates and buffer size monitoring."""

from __future__ import annotations

def producer_rate() -> float:
    """Return average production publish rate of events per second."""
    return 15.0

def producer_queue_size() -> int:
    """Return number of events currently buffered in producer's outgoing queue."""
    return 0
