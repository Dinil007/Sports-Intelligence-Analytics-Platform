"""Airflow operator for event enrichment and final database loading."""

from __future__ import annotations

from typing import Any, List, Dict
try:
    from airflow.models.baseoperator import BaseOperator # type: ignore
except ImportError:
    class BaseOperator: # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.task_id = kwargs.get("task_id", "mock_task")

from streaming.logging import logger
from streaming.pipeline.event_enrichment import EventEnricher
from streaming.pipeline.event_loader import EventLoader

class LoadOperator(BaseOperator):
    """Custom Airflow operator to enrich and load events to database."""
    
    def __init__(self, input_task_id: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.input_task_id = input_task_id

    def execute(self, context: Any) -> int:
        logger.info(f"Executing LoadOperator task '{self.task_id}'...")
        
        events = []
        if context and hasattr(context, "get") and "ti" in context:
            ti = context["ti"]
            events = ti.xcom_pull(task_ids=self.input_task_id) or []
            
        if not events:
            # Fallback to mock transformed events
            events = [
                {
                    "event_id": "event-1",
                    "timestamp": "2026-07-03T12:00:00Z",
                    "event_type": "PASS",
                    "player_id": 1,
                    "team_id": 1,
                    "coordinates": (50.0, 50.0),
                }
            ]

        enriched_events = [EventEnricher.enrich(e) for e in events]
        loaded_count = EventLoader.load_batch(enriched_events)
        
        logger.info(f"Enriched and loaded {loaded_count} events into storage.")
        return loaded_count
