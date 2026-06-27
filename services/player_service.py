"""
services/player_service.py
===========================
Business / presentation logic for player profiles.
Wraps database/player_repository.py and guarantees:
  - All text fields default to "N/A" when unavailable.
  - All numeric fields default to "N/A" (or 0 for totals).
  - A SPORTA tier badge dict is always present.
  - No SQL is executed here.
"""

from __future__ import annotations
from database.player_repository import (
    fetch_player_profile,
    fetch_filtered_player_names,
    fetch_all_scouting_player_names,
    fetch_all_competitions,
    fetch_all_teams,
    fetch_all_seasons,
)


# ---------------------------------------------------------------------------
# Schema — single source of truth for all guaranteed profile keys.
# Every key MUST be present in a cleaned profile dict.
# Values here are the safe defaults used when the database returns None.
# ---------------------------------------------------------------------------
PROFILE_SCHEMA: dict = {
    # Identity
    "player_name":    "Unknown Player",
    "nickname":       "N/A",
    "jersey_number":  "N/A",
    "nationality":    "N/A",
    "team":           "N/A",
    # Not available in StatsBomb data
    "position":       "N/A",
    "age":            "N/A",
    "height":         "N/A",
    "weight":         "N/A",
    "preferred_foot": "N/A",
    # Performance
    "matches_played": "N/A",
    "sporta_score":   "N/A",
    "goals":          "N/A",
    "total_xg":       "N/A",
    "passes":         "N/A",
    "shots":          "N/A",
    "carries":        "N/A",
    "pressures":      "N/A",
    "recoveries":     "N/A",
    "dribbles":       "N/A",
    # Tier badge dict
    "sporta_tier":    {"label": "Unranked", "color": "#64748b"},
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_player_profile(player_name: str) -> dict:
    """
    Return a cleaned, display-ready profile dict for *player_name*.

    Guaranteed keys (never raises KeyError in the UI):
      player_name, nickname, jersey_number, nationality, team,
      position, age, height, weight, preferred_foot,
      matches_played, sporta_score, goals, total_xg,
      passes, shots, carries, pressures, recoveries, dribbles,
      sporta_tier  -> {"label": str, "color": str}
    """
    raw = fetch_player_profile(player_name)
    return _clean(raw)


def get_filtered_players(
    position=None,
    age_min=None,
    age_max=None,
    club=None,
    competition=None,
    season=None,
):
    try:
        return fetch_filtered_player_names(
            position=position,
            age_min=age_min,
            age_max=age_max,
            club=club,
            competition=competition,
            season=season,
        )
    except Exception as e:
        print(f"get_filtered_players failed: {e}")
        return []


def get_all_competitions() -> list[str]:
    """
    Return all available competition names for filter dropdown.
    """
    return fetch_all_competitions()


def get_all_teams() -> list[str]:
    """
    Return all available team names for filter dropdown.
    """
    return fetch_all_teams()


def get_all_seasons() -> list[str]:
    """
    Return all available season names for filter dropdown.
    """
    return fetch_all_seasons()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _text(val, default: str = "N/A") -> str:
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def _num(val, decimals: int = 0, default: str = "N/A"):
    if val is None:
        return default
    try:
        f = float(val)
        if decimals:
            return round(f, decimals)
        return int(f)
    except (TypeError, ValueError):
        return default


def _sporta_tier(score) -> dict:
    try:
        s = float(score)
    except (TypeError, ValueError):
        return {"label": "Unranked", "color": "#64748b"}
    if s >= 90:
        return {"label": "Elite",            "color": "#10B981"}
    elif s >= 80:
        return {"label": "Excellent",        "color": "#3B82F6"}
    elif s >= 70:
        return {"label": "Good",             "color": "#F59E0B"}
    elif s >= 60:
        return {"label": "Average",          "color": "#8B5CF6"}
    else:
        return {"label": "Needs Improvement","color": "#EF4444"}


def _clean(raw: dict) -> dict:
    score_raw = raw.get("sporta_score")
    score     = _num(score_raw, decimals=2)

    # Start from a full copy of the schema so every key is guaranteed present
    # even if raw is empty or missing fields (e.g. DB down, no rows matched).
    result = dict(PROFILE_SCHEMA)

    result.update({
        # Identity
        "player_name":    _text(raw.get("player_name"), "Unknown Player"),
        "nickname":       _text(raw.get("nickname")),
        "jersey_number":  _num(raw.get("jersey_number")),
        "nationality":    _text(raw.get("country_name")),
        "team":           _text(raw.get("team_name")),
        # StatsBomb does not provide these fields
        "position":       _text(raw.get("position")),
        "age":            _num(raw.get("age")),
        "height":         _text(raw.get("height")),
        "weight":         _text(raw.get("weight")),
        "preferred_foot": _text(raw.get("preferred_foot")),
        # Performance
        "matches_played": _num(raw.get("matches_played")),
        "sporta_score":   score,
        "goals":          _num(raw.get("goals")),
        "total_xg":       _num(raw.get("total_xg"), decimals=2),
        "passes":         _num(raw.get("passes")),
        "shots":          _num(raw.get("shots")),
        "carries":        _num(raw.get("carries")),
        "pressures":      _num(raw.get("pressures")),
        "recoveries":     _num(raw.get("recoveries")),
        "dribbles":       _num(raw.get("dribbles")),
        # Tier badge
        "sporta_tier":    _sporta_tier(score_raw),
    })

    return result
