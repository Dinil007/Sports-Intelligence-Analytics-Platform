"""Event loader simulator for persisting events."""

from __future__ import annotations

from typing import Any, Dict, List
from streaming.logging import logger

# In-memory storage to simulate DB persistence safely
_LOADED_EVENTS_DB: List[Dict[str, Any]] = []

class EventLoader:
    """Simulates event ingestion into the database storage layer."""
    
    @staticmethod
    def load_event(event: Dict[str, Any]) -> bool:
        """Persist a single enriched event to the simulated persistence store."""
        try:
            event_copy = dict(event)
            _LOADED_EVENTS_DB.append(event_copy)
            logger.info(
                f"Successfully persisted event {event_copy.get('event_id')} "
                f"[{event_copy.get('event_type')}] to storage."
            )
            return True
        except Exception as e:
            logger.error(f"Failed to persist event to storage: {e}")
            return False

    @staticmethod
    def load_batch(events: List[Dict[str, Any]]) -> int:
        """Persist a batch of enriched events to the simulated persistence store."""
        success_count = 0
        for event in events:
            if EventLoader.load_event(event):
                success_count += 1
        logger.info(f"Batch load complete: {success_count}/{len(events)} events persisted.")
        return success_count

    @staticmethod
    def get_persisted_events() -> List[Dict[str, Any]]:
        """Retrieve all events that have been persisted during execution."""
        return list(_LOADED_EVENTS_DB)

    @staticmethod
    def clear_database() -> None:
        """Clear the in-memory simulated database."""
        _LOADED_EVENTS_DB.clear()
        logger.info("Simulated event database cleared.")
