"""Configurable micro-batching utility for stream events."""

from __future__ import annotations

from typing import Generic, List, TypeVar, Optional
from datetime import datetime
from streaming.utils.time_utils import get_utc_now

T = TypeVar("T")

class EventBatcher(Generic[T]):
    """Buffers stream items until limit is reached or time threshold is exceeded."""
    
    def __init__(self, batch_size: int, max_linger_seconds: float = 2.0) -> None:
        self.batch_size = max(1, batch_size)
        self.max_linger_seconds = max_linger_seconds
        self._buffer: List[T] = []
        self._last_flush_time: datetime = get_utc_now()
        
    def add(self, item: T) -> Optional[List[T]]:
        """Add an item to the buffer and return batch if flush criteria are met."""
        self._buffer.append(item)
        if len(self._buffer) >= self.batch_size:
            return self.flush()
        return None
        
    def check_and_flush(self) -> Optional[List[T]]:
        """Flush the batch if linger threshold has been exceeded."""
        elapsed = (get_utc_now() - self._last_flush_time).total_seconds()
        if elapsed >= self.max_linger_seconds and self._buffer:
            return self.flush()
        return None
        
    def flush(self) -> List[T]:
        """Force flush current buffer items."""
        batch = self._buffer
        self._buffer = []
        self._last_flush_time = get_utc_now()
        return batch

    def size(self) -> int:
        """Return current buffered count."""
        return len(self._buffer)
