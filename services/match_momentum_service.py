"""
services/match_momentum_service.py
==================================
Deterministic Match Momentum & Game Flow Analytics calculations.

No SQL. No repositories. No ML. No AI. All functions consume the events list
provided by get_match_dashboard()["events"].
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0
FINAL_THIRD_X = 80.0
PROGRESSIVE_GAIN = 10.0


def _team_name(event: dict[str, Any]) -> str | None:
    team = event.get("team_name")
    return str(team) if team else None


def _minute(event: dict[str, Any]) -> int:
    try:
        minute = int(event.get("minute") or 0)
    except (TypeError, ValueError):
        minute = 0
    return max(0, minute)


def _location(event: dict[str, Any], key: str = "location") -> list[float] | None:
    loc = event.get(key)
    if isinstance(loc, (list, tuple)) and len(loc) >= 2:
        try:
            return [float(loc[0]), float(loc[1])]
        except (TypeError, ValueError):
            return None
    return None


def _end_location(event: dict[str, Any]) -> list[float] | None:
    event_type = event.get("event_type")
    if event_type == "Pass":
        return _location(event, "pass_end_location")
    if event_type == "Carry":
        return _location(event, "carry_end_location")
    return _location(event, "pass_end_location") or _location(event, "carry_end_location")


def _teams(events: list[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for event in events:
        team = _team_name(event)
        if team and team not in seen:
            seen.add(team)
            result.append(team)
    return result


def _minute_range(events: list[dict[str, Any]]) -> list[int]:
    max_minute = max((_minute(event) for event in events), default=0)
    return list(range(max_minute + 1))


def _is_goal(event: dict[str, Any]) -> bool:
    values = [event.get("event_type"), event.get("shot_outcome"), event.get("outcome"), event.get("result")]
    return any(str(value).lower() == "goal" for value in values if value is not None)


def _is_duel_won(event: dict[str, Any]) -> bool:
    if event.get("event_type") != "Duel":
        return False
    values = [event.get("duel_outcome"), event.get("outcome"), event.get("result")]
    return any("won" in str(value).lower() for value in values if value is not None)


def _progressive_gain(event: dict[str, Any]) -> float:
    start = _location(event)
    end = _end_location(event)
    if not start or not end:
        return 0.0
    return max(0.0, end[0] - start[0])


def _is_progressive_action(event: dict[str, Any]) -> bool:
    return event.get("event_type") in {"Pass", "Carry"} and _progressive_gain(event) >= PROGRESSIVE_GAIN


def _is_final_third_entry(event: dict[str, Any]) -> bool:
    start = _location(event)
    end = _end_location(event)
    if not start or not end:
        return False
    return start[0] < FINAL_THIRD_X <= end[0]


def _is_dangerous_attack(event: dict[str, Any]) -> bool:
    event_type = event.get("event_type")
    loc = _location(event)
    end = _end_location(event)
    if event_type == "Shot":
        return True
    if event_type in {"Pass", "Carry"} and (_is_final_third_entry(event) or _is_progressive_action(event)):
        return True
    if loc and loc[0] >= FINAL_THIRD_X and event_type in {"Pressure", "Ball Recovery"}:
        return True
    if end and end[0] >= FINAL_THIRD_X and event_type in {"Pass", "Carry"}:
        return True
    return False


def _event_weight(event: dict[str, Any]) -> float:
    event_type = event.get("event_type")
    score = 0.0
    if event_type == "Shot":
        score += 5.0
    elif event_type == "Pass":
        score += 0.2
    elif event_type == "Carry":
        score += 0.4
    elif event_type == "Pressure":
        score += 1.0
    elif event_type == "Ball Recovery":
        score += 2.0
    elif _is_duel_won(event):
        score += 1.5

    if _is_goal(event):
        score += 10.0
    if _is_progressive_action(event):
        score += 2.0
    if _is_final_third_entry(event):
        score += 1.0
    return score


def calculate_match_momentum(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate weighted momentum score by minute and team."""
    teams = _teams(events)
    minutes = _minute_range(events)
    scores: dict[str, list[float]] = {team: [0.0 for _ in minutes] for team in teams}

    for event in events:
        team = _team_name(event)
        if not team or team not in scores:
            continue
        minute = _minute(event)
        if minute >= len(minutes):
            continue
        scores[team][minute] += _event_weight(event)

    for team, values in scores.items():
        scores[team] = [round(value, 2) for value in values]

    return {"minutes": minutes, "teams": scores}


def calculate_possession_flow(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Estimate possession share by minute from team-tagged event counts."""
    teams = _teams(events)
    minutes = _minute_range(events)
    counts: dict[str, list[int]] = {team: [0 for _ in minutes] for team in teams}

    for event in events:
        team = _team_name(event)
        if team and team in counts:
            counts[team][_minute(event)] += 1

    shares: dict[str, list[float]] = {team: [] for team in teams}
    for idx in range(len(minutes)):
        total = sum(counts[team][idx] for team in teams)
        for team in teams:
            value = (counts[team][idx] / total * 100.0) if total else 0.0
            shares[team].append(round(value, 1))

    return {"minutes": minutes, "teams": shares}


def calculate_dangerous_attacks(events: list[dict[str, Any]]) -> dict[str, int]:
    """Count dangerous attacks by team."""
    counts: dict[str, int] = defaultdict(int)
    for event in events:
        team = _team_name(event)
        if team and _is_dangerous_attack(event):
            counts[team] += 1
    return dict(counts)


def calculate_final_third_entries(events: list[dict[str, Any]]) -> dict[str, int]:
    """Count pass and carry entries into the attacking third by team."""
    counts: dict[str, int] = defaultdict(int)
    for event in events:
        team = _team_name(event)
        if team and _is_final_third_entry(event):
            counts[team] += 1
    return dict(counts)


def calculate_ball_progression(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate cumulative forward progression by minute and team."""
    teams = _teams(events)
    minutes = _minute_range(events)
    gains: dict[str, list[float]] = {team: [0.0 for _ in minutes] for team in teams}

    for event in events:
        team = _team_name(event)
        if not team or team not in gains or event.get("event_type") not in {"Pass", "Carry"}:
            continue
        gain = _progressive_gain(event)
        if gain >= PROGRESSIVE_GAIN:
            gains[team][_minute(event)] += gain

    cumulative: dict[str, list[float]] = {}
    for team, values in gains.items():
        running = 0.0
        cumulative[team] = []
        for value in values:
            running += value
            cumulative[team].append(round(running, 1))

    return {"minutes": minutes, "teams": cumulative}


def calculate_pressure_timeline(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Count pressure events by minute and team."""
    teams = _teams(events)
    minutes = _minute_range(events)
    pressures: dict[str, list[int]] = {team: [0 for _ in minutes] for team in teams}

    for event in events:
        team = _team_name(event)
        if team and team in pressures and event.get("event_type") == "Pressure":
            pressures[team][_minute(event)] += 1

    return {"minutes": minutes, "teams": pressures}


def calculate_attacking_direction(events: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Count attacking actions by horizontal lane and team."""
    lanes = ["Left Wing", "Half Space Left", "Central", "Half Space Right", "Right Wing"]
    result: dict[str, dict[str, int]] = {team: {lane: 0 for lane in lanes} for team in _teams(events)}

    for event in events:
        team = _team_name(event)
        if not team or team not in result:
            continue
        if event.get("event_type") not in {"Shot", "Pass", "Carry", "Pressure", "Ball Recovery"}:
            continue
        loc = _end_location(event) or _location(event)
        if not loc or loc[0] < FINAL_THIRD_X:
            continue
        y = max(0.0, min(PITCH_WIDTH, loc[1]))
        if y < 16:
            lane = "Left Wing"
        elif y < 32:
            lane = "Half Space Left"
        elif y < 48:
            lane = "Central"
        elif y < 64:
            lane = "Half Space Right"
        else:
            lane = "Right Wing"
        result[team][lane] += 1

    return result


def calculate_momentum_kpis(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate headline momentum KPIs."""
    momentum = calculate_match_momentum(events)
    teams = momentum.get("teams", {})
    totals = {team: sum(values) for team, values in teams.items()}
    dominant_team = max(totals, key=totals.get) if totals else "N/A"

    leaders: list[str | None] = []
    for idx in range(len(momentum.get("minutes", []))):
        minute_scores = {team: values[idx] for team, values in teams.items() if idx < len(values)}
        leader = max(minute_scores, key=minute_scores.get) if minute_scores and max(minute_scores.values()) > 0 else None
        leaders.append(leader)

    swings = 0
    previous = None
    for leader in leaders:
        if leader is None:
            continue
        if previous is not None and leader != previous:
            swings += 1
        previous = leader

    possession_lengths: list[int] = []
    current_team = None
    current_length = 0
    progressive_actions = 0
    for event in sorted(events, key=lambda item: (_minute(item), item.get("second") or 0)):
        team = _team_name(event)
        if team != current_team:
            if current_length:
                possession_lengths.append(current_length)
            current_team = team
            current_length = 1 if team else 0
        elif team:
            current_length += 1
        if _is_progressive_action(event):
            progressive_actions += 1
    if current_length:
        possession_lengths.append(current_length)

    avg_possession_length = round(sum(possession_lengths) / len(possession_lengths), 1) if possession_lengths else 0.0
    dangerous_attacks = sum(calculate_dangerous_attacks(events).values())
    final_third_entries = sum(calculate_final_third_entries(events).values())

    return {
        "dominant_team": dominant_team,
        "momentum_swings": swings,
        "dangerous_attacks": dangerous_attacks,
        "average_possession_length": avg_possession_length,
        "final_third_entries": final_third_entries,
        "progressive_actions": progressive_actions,
    }


def generate_match_momentum_summary(events: list[dict[str, Any]]) -> str:
    """Generate a concise deterministic momentum summary."""
    if not events:
        return "No event data is available for match momentum analysis."

    momentum = calculate_match_momentum(events)
    kpis = calculate_momentum_kpis(events)
    minutes = momentum.get("minutes", [])
    teams = list(momentum.get("teams", {}).keys())
    if not teams:
        return "No team-tagged events are available for match momentum analysis."

    split_minute = 30
    first_phase = {}
    second_phase = {}
    for team, values in momentum["teams"].items():
        first_phase[team] = sum(value for minute, value in zip(minutes, values) if minute <= split_minute)
        second_phase[team] = sum(value for minute, value in zip(minutes, values) if minute > split_minute)

    early_team = max(first_phase, key=first_phase.get) if first_phase else "N/A"
    late_team = max(second_phase, key=second_phase.get) if second_phase else early_team
    swings = kpis.get("momentum_swings", 0)
    dominant = kpis.get("dominant_team", "N/A")

    if early_team == late_team:
        return (
            f"{dominant} carried the strongest overall momentum through sustained attacking activity. "
            f"The same side led the main momentum phases, with {swings} momentum swings across the match."
        )

    return (
        f"{early_team} controlled the opening 30 minutes through stronger event momentum. "
        f"{late_team} gained momentum later through increased attacking activity and pressure. "
        f"Overall momentum shifted {swings} times during the match."
    )


__all__ = [
    "calculate_match_momentum",
    "calculate_possession_flow",
    "calculate_dangerous_attacks",
    "calculate_final_third_entries",
    "calculate_ball_progression",
    "calculate_pressure_timeline",
    "calculate_attacking_direction",
    "calculate_momentum_kpis",
    "generate_match_momentum_summary",
]
