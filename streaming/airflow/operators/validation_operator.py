"""Airflow operator for event validation and transformation."""

from __future__ import annotations

from typing import Any, List, Dict
try:
    from airflow.models.baseoperator import BaseOperator # type: ignore
except ImportError:
    class BaseOperator: # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.task_id = kwargs.get("task_id", "mock_task")

from streaming.logging import logger
from streaming.pipeline.event_validator import EventValidator
from streaming.pipeline.event_transformer import EventTransformer

class ValidationOperator(BaseOperator):
    """Custom Airflow operator to validate and transform event batches."""
    
    def __init__(self, input_task_id: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.input_task_id = input_task_id

    def execute(self, context: Any) -> List[Dict[str, Any]]:
        logger.info(f"Executing ValidationOperator task '{self.task_id}'...")
        
        # In real Airflow, retrieve events from XCom
        # In this wrapper, we pull from context if available, or fallback to mock list
        events = []
        if context and hasattr(context, "get") and "ti" in context:
            ti = context["ti"]
            events = ti.xcom_pull(task_ids=self.input_task_id) or []
            
        if not events:
            # Fallback to mock events for stand-alone execution
            events = [
                {
                    "event_id": "event-1",
                    "timestamp": "2026-07-03T12:00:00Z",
                    "event_type": "PASS",
                    "player_id": 1,
                    "team_id": 1,
                    "coordinates": [50.0, 50.0],
                }
            ]

        valid_events = []
        for event in events:
            is_valid, err = EventValidator.validate_event(event)
            if is_valid:
                transformed = EventTransformer.transform(event)
                valid_events.append(transformed)
            else:
                logger.warning(f"Event validation failed during DAG run: {err}")
                
        logger.info(f"Validated and transformed {len(valid_events)}/{len(events)} events.")
        return valid_events
