"""Manager for starting and stopping ingestion and metrics reporting."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from streaming.logging import logger
from streaming.pipeline.event_processor import EventProcessor
from streaming.models.pipeline_status import PipelineStatus
from streaming.utils.time_utils import get_utc_now

class PipelineManager:
    """Manages stream processing pipeline runs and statistics monitoring."""
    
    def __init__(self, pipeline_id: str = "live-football-ingest") -> None:
        self.pipeline_id = pipeline_id
        self.is_active = False
        self.processed_count = 0
        self.error_count = 0
        self.start_time: Optional[datetime] = None
        self.last_event_time: Optional[datetime] = None
        
        # Internal performance stats
        self.latencies: List[float] = []

    def start_pipeline(self) -> None:
        """Start the pipeline execution state."""
        self.is_active = True
        self.start_time = get_utc_now()
        self.last_event_time = get_utc_now()
        logger.info(f"Pipeline '{self.pipeline_id}' started at {self.start_time}")

    def stop_pipeline(self) -> None:
        """Stop the pipeline execution state."""
        self.is_active = False
        logger.info(f"Pipeline '{self.pipeline_id}' stopped. Processed: {self.processed_count}, Errors: {self.error_count}")

    def ingest_event(self, event: Dict[str, Any]) -> bool:
        """Ingest a single event into the pipeline."""
        if not self.is_active:
            logger.warning("Pipeline is not active. Discarding event.")
            return False
            
        t0 = time.perf_counter()
        success, _, err = EventProcessor.process_event(event)
        latency = time.perf_counter() - t0
        self.latencies.append(latency)
        
        # Keep sliding window of latencies to prevent memory bloat
        if len(self.latencies) > 1000:
            self.latencies.pop(0)
            
        self.last_event_time = get_utc_now()
        if success:
            self.processed_count += 1
            return True
        else:
            self.error_count += 1
            # Publish system/pipeline event if required
            return False

    def ingest_batch(self, events: List[Dict[str, Any]]) -> int:
        """Ingest a batch of events into the pipeline."""
        success_count = 0
        for event in events:
            if self.ingest_event(event):
                success_count += 1
        return success_count

    def get_status(self) -> PipelineStatus:
        """Return the current pipeline status model."""
        uptime = 0.0
        if self.start_time:
            uptime = (get_utc_now() - self.start_time).total_seconds()
            
        return PipelineStatus(
            pipeline_id=self.pipeline_id,
            is_active=self.is_active,
            last_event_time=self.last_event_time or get_utc_now(),
            processed_count=self.processed_count,
            error_count=self.error_count,
            uptime_seconds=uptime,
        )
