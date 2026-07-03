"""Event processing pipeline wrapper."""

from __future__ import annotations

from typing import Any, Dict, Tuple, Optional
from streaming.pipeline.event_validator import EventValidator
from streaming.pipeline.event_transformer import EventTransformer
from streaming.pipeline.event_enrichment import EventEnricher
from streaming.pipeline.event_loader import EventLoader
from streaming.logging import logger

class EventProcessor:
    """Orchestrates single-event stream processing flow."""
    
    @staticmethod
    def process_event(event: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """Process a single event through validate, transform, enrich, and load.
        
        Returns:
            (success, processed_event_dict, error_reason)
        """
        # 1. Validate
        is_valid, err = EventValidator.validate_event(event)
        if not is_valid:
            logger.warning(f"Event failed validation: {err}")
            return False, None, err
            
        try:
            # 2. Transform
            transformed = EventTransformer.transform(event)
            
            # 3. Enrich
            enriched = EventEnricher.enrich(transformed)
            
            # 4. Load
            loaded = EventLoader.load_event(enriched)
            if not loaded:
                return False, enriched, "Database persistence failed"
                
            return True, enriched, None
        except Exception as e:
            logger.error(f"Execution error processing event: {e}")
            return False, None, str(e)
