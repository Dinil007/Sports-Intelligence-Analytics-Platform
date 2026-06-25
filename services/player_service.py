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
from database.player_repository import fetch_player_profile


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

    return {
        # Identity
        "player_name":    _text(raw.get("player_name"), "Unknown"),
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
    }
