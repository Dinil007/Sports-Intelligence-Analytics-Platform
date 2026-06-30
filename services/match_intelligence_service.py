"""
services/match_intelligence_service.py
========================================
Orchestrates match data retrieval and metric calculation.

Imports:
    repository  -> raw match data
    match_metrics -> calculated stats

No Streamlit. No Plotly. No HTML. No SQL.
Public interface returns plain Python dictionaries.
"""

from __future__ import annotations

from typing import Any

from database.match_repository import (
    fetch_match,
    fetch_match_events,
    fetch_match_lineups,
    fetch_match_players,
    fetch_team_statistics,
    fetch_player_statistics,
)
from ml.match_metrics import (
    calculate_possession,
    calculate_pass_accuracy,
    calculate_shot_accuracy,
    calculate_ppda,
    calculate_pressures,
    calculate_progressive_passes,
    calculate_team_summary,
)


def get_match_dashboard(match_id: int) -> dict[str, Any]:
    """Build the complete match intelligence dashboard data package.

    Parameters
    ----------
    match_id : int
        The StatsBomb match identifier.

    Returns
    -------
    dict
        {
            "match_info": {...},
            "home_team": "...",
            "away_team": "...",
            "score": {"home": int, "away": int},
            "team_statistics": {...},
            "player_statistics": [...],
            "timeline": [...],
            "events": [...],
        }

    Returns a dict with empty / None values when data is unavailable.
    """
    match = fetch_match(match_id)
    if not match:
        return {
            "match_info": None,
            "home_team": None,
            "away_team": None,
            "score": {},
            "team_statistics": {},
            "player_statistics": [],
            "timeline": [],
            "events": [],
        }

    team_stats = fetch_team_statistics(match_id)
    raw_metrics = calculate_team_summary(fetch_match_events(match_id))

    # Merge repository stats with ML-computed metrics
    merged_team_stats = {
        "repository": team_stats,
        "metrics": raw_metrics,
        "possession": calculate_possession(fetch_match_events(match_id)),
        "pass_accuracy": calculate_pass_accuracy(fetch_match_events(match_id)),
        "shot_accuracy": calculate_shot_accuracy(fetch_match_events(match_id)),
        "ppda": calculate_ppda(fetch_match_events(match_id)),
        "pressures": calculate_pressures(fetch_match_events(match_id)),
        "progressive_passes": calculate_progressive_passes(fetch_match_events(match_id)),
    }

    # Timeline = events sorted by minute (deduped for readability)
    raw_events = fetch_match_events(match_id)
    seen = set()
    timeline = []
    for e in raw_events:
        key = (e.get("minute"), e.get("event_type"), e.get("player_name"))
        if key not in seen:
            seen.add(key)
            timeline.append({
                "minute": e.get("minute"),
                "event_type": e.get("event_type"),
                "player_name": e.get("player_name"),
                "team_name": e.get("team_name"),
                "period": e.get("period"),
            })

    return {
        "match_info": match,
        "home_team": match["home_team"],
        "away_team": match["away_team"],
        "score": {
            "home": match["home_score"],
            "away": match["away_score"],
        },
        "team_statistics": merged_team_stats,
        "player_statistics": fetch_player_statistics(match_id),
        "timeline": timeline,
        "events": raw_events,
    }
