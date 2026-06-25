"""
services/player_service.py
===========================
Business logic layer for player profiles.
Cleans raw DB rows, fills missing values with 'N/A',
and returns structured dicts safe for UI consumption.
"""

from __future__ import annotations

from database.player_repository import fetch_player_profile, fetch_player_stats


# ---------------------------------------------------------------------------
# Field definitions  (label → DB key)
# ---------------------------------------------------------------------------

_NA = "N/A"

_PROFILE_FIELDS: list[tuple[str, str]] = [
    ("Full Name",      "player_name"),
    ("Known As",       "nickname"),
    ("Nationality",    "nationality"),
    ("Club / Team",    "team_name"),
    ("Jersey No.",     "jersey_number"),
    ("Position",       "position"),        # not in DB → always N/A
    ("Age",            "age"),             # not in DB → always N/A
    ("Height",         "height"),          # not in DB → always N/A
    ("Preferred Foot", "preferred_foot"),  # not in DB → always N/A
]

_STAT_FIELDS: list[tuple[str, str]] = [
    ("Matches Played", "matches_played"),
    ("Goals",          "goals"),
    ("Expected Goals", "total_xg"),
    ("Passes",         "passes"),
    ("Shots",          "shots"),
    ("Carries",        "carries"),
    ("Dribbles",       "dribbles"),
    ("Pressures",      "pressures"),
    ("Recoveries",     "recoveries"),
    ("SPORTA Score",   "sporta_score"),
]


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _clean(value) -> str:
    """Return a display-safe string, or 'N/A' for None / empty."""
    if value is None:
        return _NA
    s = str(value).strip()
    return s if s not in ("", "None", "nan") else _NA


def _fmt_float(value, decimals: int = 2) -> str:
    """Format a numeric value to fixed decimals, or 'N/A'."""
    if value is None:
        return _NA
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return _NA


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_player_profile(player_name: str) -> dict:
    """
    Return a fully-cleaned player profile dict.

    Keys present:
        profile_fields : list of (label, value_str) tuples for the card
        stat_fields    : list of (label, value_str) tuples for KPI section
        raw            : the raw DB dict (for internal calculations)
        found          : bool – whether the player was found in dim_players
        display_name   : short display name (nickname if available, else full)
        initials       : 2-char initials string for avatar
        sporta_score   : float | None
        sporta_tier    : (label, hex_color) tuple
    """
    raw = fetch_player_profile(player_name)

    # Fall back to stats-only if not in dim_players
    if not raw:
        raw = fetch_player_stats(player_name)

    found = bool(raw)

    # Display name
    nickname = _clean(raw.get("nickname"))
    full_name = _clean(raw.get("player_name", player_name))
    display_name = nickname if nickname != _NA else full_name

    # Initials
    parts = display_name.split()
    initials = "".join(p[0] for p in parts[:2]).upper() or "P"

    # Profile card rows
    profile_fields: list[tuple[str, str]] = []
    for label, key in _PROFILE_FIELDS:
        if key in ("total_xg",):
            profile_fields.append((label, _fmt_float(raw.get(key))))
        elif key == "jersey_number":
            v = raw.get(key)
            profile_fields.append((label, str(int(v)) if v is not None else _NA))
        else:
            profile_fields.append((label, _clean(raw.get(key))))

    # Stat rows
    stat_fields: list[tuple[str, str]] = []
    for label, key in _STAT_FIELDS:
        v = raw.get(key)
        if key in ("total_xg", "sporta_score"):
            stat_fields.append((label, _fmt_float(v)))
        elif v is not None:
            try:
                stat_fields.append((label, str(int(float(v)))))
            except (TypeError, ValueError):
                stat_fields.append((label, _clean(v)))
        else:
            stat_fields.append((label, _NA))

    # SPORTA Score
    sc_raw = raw.get("sporta_score")
    try:
        sporta_score: float | None = float(sc_raw) if sc_raw is not None else None
    except (TypeError, ValueError):
        sporta_score = None

    tier = _sporta_tier(sporta_score)

    return {
        "raw":           raw,
        "found":         found,
        "display_name":  display_name,
        "full_name":     full_name,
        "initials":      initials,
        "profile_fields": profile_fields,
        "stat_fields":   stat_fields,
        "sporta_score":  sporta_score,
        "sporta_tier":   tier,
    }


def _sporta_tier(score: float | None) -> tuple[str, str]:
    if score is None:
        return ("Unranked", "#6B7280")
    if score >= 90:
        return ("Elite",            "#10B981")
    if score >= 80:
        return ("Excellent",        "#3B82F6")
    if score >= 70:
        return ("Good",             "#F59E0B")
    if score >= 60:
        return ("Average",          "#8B5CF6")
    return ("Needs Improvement",    "#EF4444")
