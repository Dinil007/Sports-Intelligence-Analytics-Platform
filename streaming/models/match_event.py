"""Pydantic model representing specific football match event details."""

from __future__ import annotations

from typing import Dict, Any, Optional, Tuple
from pydantic import Field
from streaming.models.stream_event import StreamEvent

class MatchEvent(StreamEvent):
    """Specific event representing a live match occurrence (passes, shots, etc.)."""
    match_id: int = Field(..., description="ID of the match")
    player_id: Optional[int] = Field(None, description="Database ID of the player involved")
    team_id: Optional[int] = Field(None, description="Database ID of the team involved")
    coordinates: Optional[Tuple[float, float]] = Field(None, description="X, Y coordinates on pitch (0-100 scale)")
    
    # Enrichment fields (optional, populated by pipeline)
    player_name: Optional[str] = Field(None, description="Enriched player name")
    team_name: Optional[str] = Field(None, description="Enriched team name")
    competition: Optional[str] = Field(None, description="Enriched competition name")
    season: Optional[str] = Field(None, description="Enriched season name")
    position: Optional[str] = Field(None, description="Enriched player position")
