"""Event enrichment using existing platform services without raw SQL."""

from __future__ import annotations

from typing import Any, Dict
from streaming.logging import logger

# Mock DB mapping for player_id / team_id mapping when only IDs are in the stream
MOCK_PLAYER_DB = {
    1: {"player_name": "Lionel Andrés Messi Cuccittini", "position": "Forward", "team": "Barcelona"},
    2: {"player_name": "Neymar da Silva Santos Junior", "position": "Forward", "team": "Barcelona"},
    3: {"player_name": "Luis Alberto Suárez Díaz", "position": "Forward", "team": "Barcelona"},
}

MOCK_TEAM_DB = {
    1: "Barcelona",
    2: "Real Madrid",
    3: "Atletico Madrid",
}

class EventEnricher:
    """Enriches event streams with player, team, competition, and season metadata."""
    
    @staticmethod
    def enrich(event: Dict[str, Any]) -> Dict[str, Any]:
        """Add context (names, competition, season, position) using cached data or services."""
        enriched = dict(event)
        
        player_id = enriched.get("player_id")
        team_id = enriched.get("team_id")
        
        # 1. Resolve team info
        if team_id and not enriched.get("team_name"):
            enriched["team_name"] = MOCK_TEAM_DB.get(int(team_id), "Unknown Club")
            
        # 2. Resolve player info using mock or player_service
        p_info = None
        if player_id:
            p_info = MOCK_PLAYER_DB.get(int(player_id))
            
        if p_info:
            if not enriched.get("player_name"):
                enriched["player_name"] = p_info["player_name"]
            if not enriched.get("position"):
                enriched["position"] = p_info["position"]
            if not enriched.get("team_name") and p_info.get("team"):
                enriched["team_name"] = p_info["team"]

        # If player_name is available, try to resolve via services.player_service
        player_name = enriched.get("player_name")
        if player_name:
            try:
                from services.player_service import get_player_profile
                profile = get_player_profile(player_name)
                if profile and profile.get("player_name") != "Unknown Player":
                    enriched["position"] = profile.get("position", enriched.get("position", "N/A"))
                    enriched["team_name"] = profile.get("team", enriched.get("team_name", "N/A"))
                    enriched["metadata"]["sporta_score"] = profile.get("sporta_score")
            except Exception as e:
                logger.warning(f"Failed to enrich player profile for '{player_name}' using player_service: {e}")

        # 3. Add default competition and season if not present
        if not enriched.get("competition"):
            enriched["competition"] = "La Liga"
        if not enriched.get("season"):
            enriched["season"] = "2015/2016"
            
        return enriched
