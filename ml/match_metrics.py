"""
ml/match_metrics.py
====================
Pure calculation helpers for Match Intelligence.

No SQL. No Streamlit. No Plotly. No ML model inference.
Receives pre-fetched event lists and returns plain Python dictionaries.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any


# ---------------------------------------------------------------------------
# Individual metric calculators
# ---------------------------------------------------------------------------


def calculate_possession(events: list[dict[str, Any]]) -> dict[str, float | None]:
    """Average possession sequence per team.

    Returns ``{team_name: avg_possession}`` where avg_possession is the
    mean of all ``possession`` column values for that team, or ``None``
    when the source data does not carry possession numbers.
    """
    buckets: dict[str, list[int]] = defaultdict(list)
    for e in events:
        team = e.get("team_name")
        if not team:
            continue
        p = e.get("possession")
        if p is not None:
            buckets[team].append(int(p))

    return {team: (sum(v) / len(v) if v else None) for team, v in buckets.items()}


def calculate_pass_accuracy(events: list[dict[str, Any]]) -> dict[str, float | None]:
    """Return ``{team_name: completion_pct}``.

    The current StatsBomb schema does not include pass outcomes, so this
    returns ``None`` for every team as a placeholder for future enhancement.
    """
    teams = sorted({e.get("team_name") for e in events if e.get("team_name")})
    return {t: None for t in teams}


def calculate_shot_accuracy(events: list[dict[str, Any]]) -> dict[str, float | None]:
    """Return ``{team_name: accuracy_pct}``.

    The current StatsBomb schema does not include shot outcomes, so this
    returns ``None`` for every team as a placeholder for future enhancement.
    """
    teams = sorted({e.get("team_name") for e in events if e.get("team_name")})
    return {t: None for t in teams}


def calculate_ppda(events: list[dict[str, Any]]) -> dict[str, float | None]:
    """Passes Per Defensive Action.

    PPDA = opponent_pass_count / defensive_actions
    Defensive actions are approximated as ``Pressure`` events.
    Returns ``{team_name: ppda}``. Higher = weaker press.
    """
    opponents_passes: dict[str, int] = defaultdict(int)
    defensive_actions: dict[str, int] = defaultdict(int)

    for e in events:
        team = e.get("team_name")
        if not team:
            continue
        et = e.get("event_type", "")
        if et == "Pass":
            opponents_passes[team] += 1
        if et == "Pressure":
            defensive_actions[team] += 1

    result: dict[str, float | None] = {}
    for team in opponents_passes:
        da = defensive_actions.get(team, 0)
        result[team] = opponents_passes[team] / da if da > 0 else None
    return result


def calculate_pressures(events: list[dict[str, Any]]) -> dict[str, int]:
    """Return ``{team_name: pressure_count}``."""
    counts: dict[str, int] = defaultdict(int)
    for e in events:
        team = e.get("team_name")
        if team and e.get("event_type") == "Pressure":
            counts[team] += 1
    return dict(counts)


def calculate_progressive_passes(events: list[dict[str, Any]]) -> dict[str, int]:
    """Return ``{team_name: progressive_pass_count}``.

    Current schema does not expose pass start/end coordinates, so this
    returns a total pass count as a stand-in for now.
    """
    counts: dict[str, int] = defaultdict(int)
    for e in events:
        team = e.get("team_name")
        if team and e.get("event_type") == "Pass":
            counts[team] += 1
    return dict(counts)


def calculate_xg(events: list[dict[str, Any]]) -> dict[str, float]:
    """Return ``{team_name: total_xg}``.

    Current schema does not include xG values per shot, so this
    returns ``0.0`` for every team as a placeholder.
    """
    teams = sorted({e.get("team_name") for e in events if e.get("team_name")})
    return {t: 0.0 for t in teams}


def calculate_team_summary(
    events: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Return a per-team summary aggregating all available metrics.

    Returns
    -------
    dict[str, dict[str, Any]]
        Keys are team names. Values are dicts of aggregated stats.
    """
    if not events:
        return {}

    teams = sorted({e.get("team_name") for e in events if e.get("team_name")})
    result: dict[str, dict[str, Any]] = {}

    for team in teams:
        team_evs = [e for e in events if e.get("team_name") == team]
        result[team] = {
            "team_name": team,
            "total_events": len(team_evs),
            "passes": sum(1 for e in team_evs if e.get("event_type") == "Pass"),
            "shots": sum(1 for e in team_evs if e.get("event_type") == "Shot"),
            "pressures": sum(1 for e in team_evs if e.get("event_type") == "Pressure"),
            "carries": sum(1 for e in team_evs if e.get("event_type") == "Carry"),
            "dribbles": sum(1 for e in team_evs if e.get("event_type") == "Dribble"),
            "recoveries": sum(1 for e in team_evs if e.get("event_type") == "Ball Recovery"),
            "fouls_committed": sum(1 for e in team_evs if e.get("event_type") == "Foul Committed"),
            "fouls_won": sum(1 for e in team_evs if e.get("event_type") == "Foul Won"),
        }

    return result
