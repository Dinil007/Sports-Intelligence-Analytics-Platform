"""Pydantic model for monitoring streaming pipeline health status."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

class PipelineStatus(BaseModel):
    """Schema representing the status and metrics of a running pipeline."""
    pipeline_id: str = Field(..., description="Unique name/identifier of the pipeline")
    is_active: bool = Field(True, description="True if pipeline is currently consuming")
    last_event_time: datetime = Field(..., description="Timestamp of the last successfully processed event")
    processed_count: int = Field(0, description="Total number of events processed")
    error_count: int = Field(0, description="Total validation/processing failures")
    uptime_seconds: float = Field(0.0, description="Uptime of the processor in seconds")
