"""Pydantic model representing base stream events."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class StreamEvent(BaseModel):
    """Base schema for all events flowing through the streaming platform."""
    event_id: str = Field(..., description="Unique UUID or identifier for the event")
    timestamp: datetime = Field(..., description="UTC ISO timestamp of the event")
    event_type: str = Field(..., description="Type of event (e.g. PASS, SHOT, SYSTEM)")
    source: str = Field("sporta-stream", description="Source of the event")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional arbitrary metadata")
