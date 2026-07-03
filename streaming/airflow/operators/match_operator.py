"""Airflow operator for match event extraction."""

from __future__ import annotations

from typing import Any

# Try importing Airflow BaseOperator; fallback to mock BaseOperator if missing
try:
    from airflow.models.baseoperator import BaseOperator # type: ignore
except ImportError:
    class BaseOperator: # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.task_id = kwargs.get("task_id", "mock_task")

from streaming.logging import logger
from streaming.airflow.utils.pipeline_utils import extract_live_batch

class MatchOperator(BaseOperator):
    """Custom Airflow operator to extract match events."""
    
    def __init__(self, match_id: int, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.match_id = match_id

    def execute(self, context: Any) -> list:
        logger.info(f"Executing MatchOperator task '{self.task_id}' for match_id: {self.match_id}")
        events = extract_live_batch(self.match_id)
        logger.info(f"Extracted {len(events)} events.")
        return events
