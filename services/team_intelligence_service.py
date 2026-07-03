"""
services/team_intelligence_service.py
=====================================
Deterministic Team Intelligence & Tactical Pattern Analysis calculations.

All public functions consume match_dashboard["events"] only. No SQL, repositories,
ML, AI, or external services are used here.
"""

from __future__ import annotations

from collections import defaultdict
from math import sqrt
from typing import Any

PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0
PROGRESSIVE_GAIN = 10.0
FINAL_THIRD_X = 80.0
SHOT_TYPES = {"Shot"}
DEFENSIVE_ACTIONS = {"Pressure", "Ball Recovery", "Interception", "Block", "Clearance", "Duel", "Tackle"}
TURNOVER_OUTCOMES = {"incomplete", "out", "lost", "offside", "pass offside", "unknown"}


def _team(event: dict[str, Any]) -> str | None:
    team = event.get("team_name") or event.get("team")
    return str(team) if team else None


def _player(event: dict[str, Any]) -> str:
    return str(event.get("player_name") or event.get("player") or "Unknown")


def _event_type(event: dict[str, Any]) -> str:
    return str(event.get("event_type") or event.get("type") or "")


def _minute(event: dict[str, Any]) -> int:
    try:
        return max(0, int(event.get("minute") or 0))
    except (TypeError, ValueError):
        return 0


def _second(event: dict[str, Any]) -> int:
    try:
        return max(0, int(event.get("second") or 0))
    except (TypeError, ValueError):
        return 0


def _period(event: dict[str, Any]) -> int:
    try:
        return max(1, int(event.get("period") or 1))
    except (TypeError, ValueError):
        return 1


def _location(event: dict[str, Any], key: str = "location") -> tuple[float, float] | None:
    loc = event.get(key)
    if isinstance(loc, (list, tuple)) and len(loc) >= 2:
        try:
            x = min(PITCH_LENGTH, max(0.0, float(loc[0])))
            y = min(PITCH_WIDTH, max(0.0, float(loc[1])))
            return x, y
        except (TypeError, ValueError):
            return None
    return None


def _end_location(event: dict[str, Any]) -> tuple[float, float] | None:
    event_type = _event_type(event)
    if event_type == "Pass":
        return _location(event, "pass_end_location")
    if event_type == "Carry":
        return _location(event, "carry_end_location")
    return _location(event, "pass_end_location") or _location(event, "carry_end_location")


def _outcome(event: dict[str, Any]) -> str:
    values = [
        event.get("pass_outcome"),
        event.get("carry_outcome"),
        event.get("shot_outcome"),
        event.get("duel_outcome"),
        event.get("outcome"),
        event.get("result"),
    ]
    return " ".join(str(value).lower() for value in values if value)


def _is_successful_pass(event: dict[str, Any]) -> bool:
    if _event_type(event) != "Pass":
        return False
    outcome = _outcome(event)
    return not outcome or not any(value in outcome for value in TURNOVER_OUTCOMES)


def _is_turnover(event: dict[str, Any]) -> bool:
    outcome = _outcome(event)
    event_type = _event_type(event)
    if event_type in {"Dispossessed", "Miscontrol"}:
        return True
    return any(value in outcome for value in TURNOVER_OUTCOMES)


def _is_goal(event: dict[str, Any]) -> bool:
    return "goal" in _outcome(event)


def _distance(start: tuple[float, float] | None, end: tuple[float, float] | None) -> float:
    if not start or not end:
        return 0.0
    return sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)


def _progressive_gain(event: dict[str, Any]) -> float:
    start = _location(event)
    end = _end_location(event)
    if not start or not end:
        return 0.0
    return max(0.0, end[0] - start[0])


def _is_progressive(event: dict[str, Any]) -> bool:
    return _event_type(event) in {"Pass", "Carry"} and _progressive_gain(event) >= PROGRESSIVE_GAIN


def _is_final_third_entry(event: dict[str, Any]) -> bool:
    start = _location(event)
    end = _end_location(event)
    return bool(start and end and start[0] < FINAL_THIRD_X <= end[0])


def _vertical_lane(y: float) -> str:
    if y < 16:
        return "Left Wing"
    if y < 32:
        return "Left Half Space"
    if y < 48:
        return "Centre"
    if y < 64:
        return "Right Half Space"
    return "Right Wing"


def _third(x: float) -> str:
    if x < 40:
        return "Defensive Third"
    if x < 80:
        return "Middle Third"
    return "Attacking Third"


def _xt_value(location: tuple[float, float] | None) -> float:
    if not location:
        return 0.0
    x, y = location
    x_factor = (x / PITCH_LENGTH) ** 1.65
    centrality = 1.0 - min(abs(y - 40.0) / 40.0, 1.0)
    return round((0.02 + 0.58 * x_factor) * (0.72 + 0.28 * centrality), 4)


def _xt_added(event: dict[str, Any]) -> float:
    event_type = _event_type(event)
    start = _location(event)
    end = _end_location(event)
    if event_type in {"Pass", "Carry"} and start and end:
        return max(0.0, _xt_value(end) - _xt_value(start))
    if event_type == "Shot":
        return _xt_value(start) * 0.35
    return 0.0


def _teams(events: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    teams: list[str] = []
    for event in events:
        team = _team(event)
        if team and team not in seen:
            seen.add(team)
            teams.append(team)
    return teams


def _empty_team_counts(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    return defaultdict(lambda: defaultdict(float), {team: defaultdict(float) for team in _teams(events)})


def _aggregate(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    stats = _empty_team_counts(events)
    for event in events:
        team = _team(event)
        if not team:
            continue
        event_type = _event_type(event)
        stats[team]["events"] += 1
        if event_type in {"Pass", "Carry", "Shot"}:
            stats[team]["possession_actions"] += 1
        if event_type == "Pass":
            stats[team]["passes"] += 1
            if _is_successful_pass(event):
                stats[team]["completed_passes"] += 1
            if _is_progressive(event):
                stats[team]["progressive_passes"] += 1
        if event_type == "Carry":
            stats[team]["carries"] += 1
            if _is_progressive(event):
                stats[team]["progressive_carries"] += 1
        if event_type == "Shot":
            stats[team]["shots"] += 1
            if _is_goal(event):
                stats[team]["goals"] += 1
        if event_type == "Pressure":
            stats[team]["pressures"] += 1
        if event_type == "Ball Recovery":
            stats[team]["recoveries"] += 1
        if event_type in DEFENSIVE_ACTIONS:
            stats[team]["defensive_actions"] += 1
        if _is_final_third_entry(event):
            stats[team]["final_third_entries"] += 1
        stats[team]["expected_threat"] += _xt_added(event)
    return {team: dict(values) for team, values in stats.items()}


def calculate_team_statistics(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Calculate base team event statistics from match events."""
    return _aggregate(events or [])


def calculate_team_kpis(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Calculate headline team KPI values."""
    events = events or []
    stats = _aggregate(events)
    total_possession_actions = sum(team_stats.get("possession_actions", 0.0) for team_stats in stats.values())
    kpis: dict[str, dict[str, float]] = {}
    for team, values in stats.items():
        passes = values.get("passes", 0.0)
        shots = values.get("shots", 0.0)
        kpis[team] = {
            "Possession %": round((values.get("possession_actions", 0.0) / total_possession_actions * 100.0) if total_possession_actions else 0.0, 1),
            "Pass Accuracy": round((values.get("completed_passes", 0.0) / passes * 100.0) if passes else 0.0, 1),
            "Progressive Passes": int(values.get("progressive_passes", 0)),
            "Progressive Carries": int(values.get("progressive_carries", 0)),
            "Final Third Entries": int(values.get("final_third_entries", 0)),
            "Shot Conversion": round((values.get("goals", 0.0) / shots * 100.0) if shots else 0.0, 1),
            "Pressures": int(values.get("pressures", 0)),
            "Recoveries": int(values.get("recoveries", 0)),
            "Defensive Actions": int(values.get("defensive_actions", 0)),
            "Expected Threat": round(values.get("expected_threat", 0.0), 3),
        }
    return kpis


def detect_team_formation(events: list[dict[str, Any]]) -> dict[str, str]:
    """Detect team formations from deterministic average player positions."""
    player_positions: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0]))
    for event in events or []:
        team = _team(event)
        loc = _location(event)
        if not team or not loc:
            continue
        player = _player(event)
        bucket = player_positions[team][player]
        bucket[0] += loc[0]
        bucket[1] += loc[1]
        bucket[2] += 1.0

    formations: dict[str, str] = {}
    allowed = {"4-3-3", "4-2-3-1", "4-4-2", "3-5-2", "5-3-2"}
    for team, players in player_positions.items():
        averages = sorted(
            ((player, values[0] / values[2], values[1] / values[2]) for player, values in players.items() if values[2]),
            key=lambda item: item[1],
        )
        if len(averages) < 8:
            formations[team] = "Unknown"
            continue
        outfield = averages[1:11] if len(averages) >= 10 else averages[1:]
        xs = [item[1] for item in outfield]
        best_score = -1.0
        best_shape = (0, 0, 0)
        for defenders in (3, 4, 5):
            for midfielders in range(2, 6):
                forwards = len(xs) - defenders - midfielders
                if forwards < 1 or forwards > 3:
                    continue
                left_gap = xs[defenders] - xs[defenders - 1] if defenders < len(xs) else 0.0
                right_idx = defenders + midfielders
                right_gap = xs[right_idx] - xs[right_idx - 1] if right_idx < len(xs) else 0.0
                score = left_gap + right_gap
                if score > best_score:
                    best_score = score
                    best_shape = (defenders, midfielders, forwards)

        formation = f"{best_shape[0]}-{best_shape[1]}-{best_shape[2]}"
        if formation == "4-5-1":
            midfield_line = xs[best_shape[0] : best_shape[0] + best_shape[1]]
            formation = "4-2-3-1" if len(midfield_line) >= 5 and midfield_line[2] - midfield_line[1] > 4.0 else "4-3-3"
        formations[team] = formation if formation in allowed else "Unknown"
    return formations


def detect_playing_style(events: list[dict[str, Any]]) -> dict[str, str]:
    """Classify team playing style from deterministic event thresholds."""
    kpis = calculate_team_kpis(events)
    build_up = calculate_build_up_play(events)
    styles: dict[str, str] = {}
    for team, values in kpis.items():
        direct = build_up.get(team, {}).get("Direct Build-up", 0.0)
        wide = build_up.get(team, {}).get("Wide Build-up", 0.0)
        progressive = values.get("Progressive Passes", 0) + values.get("Progressive Carries", 0)
        if values.get("Pressures", 0) >= 35 and values.get("Recoveries", 0) >= 10:
            style = "High Press"
        elif values.get("Possession %", 0.0) >= 56 and values.get("Pass Accuracy", 0.0) >= 78:
            style = "Possession Football"
        elif values.get("Possession %", 0.0) <= 44 and progressive >= 18:
            style = "Counter Attack"
        elif direct >= 36:
            style = "Direct Play"
        elif values.get("Possession %", 0.0) <= 42 and values.get("Defensive Actions", 0) >= 45:
            style = "Low Block"
        elif wide >= 42:
            style = "Wing Play"
        else:
            style = "Balanced"
        styles[team] = style
    return styles


def calculate_build_up_play(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Calculate build-up characteristics as percentage shares by team."""
    counts = _empty_team_counts(events or [])
    for event in events or []:
        team = _team(event)
        if not team or _event_type(event) not in {"Pass", "Carry"}:
            continue
        start = _location(event)
        end = _end_location(event)
        if not start or not end:
            continue
        counts[team]["total"] += 1
        length = _distance(start, end)
        gain = max(0.0, end[0] - start[0])
        if length <= 15:
            counts[team]["Short Build-up"] += 1
        if length >= 28:
            counts[team]["Direct Build-up"] += 1
        if gain >= PROGRESSIVE_GAIN:
            counts[team]["Progressive Build-up"] += 1
        if start[1] < 18 or start[1] > 62 or end[1] < 18 or end[1] > 62:
            counts[team]["Wide Build-up"] += 1
        if 28 <= start[1] <= 52 and 28 <= end[1] <= 52:
            counts[team]["Central Build-up"] += 1

    categories = ["Short Build-up", "Direct Build-up", "Progressive Build-up", "Wide Build-up", "Central Build-up"]
    result: dict[str, dict[str, float]] = {}
    for team, values in counts.items():
        total = values.get("total", 0.0)
        result[team] = {category: round((values.get(category, 0.0) / total * 100.0) if total else 0.0, 1) for category in categories}
    return result


def calculate_possession_chains(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate deterministic possession chains by contiguous team events."""
    sorted_events = sorted(enumerate(events or []), key=lambda item: (_period(item[1]), _minute(item[1]), _second(item[1]), item[0]))
    chains: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for _, event in sorted_events:
        team = _team(event)
        if not team:
            continue
        event_type = _event_type(event)
        if current is None or current["team"] != team:
            if current:
                chains.append(current)
            current = {"team": team, "start_minute": _minute(event), "end_minute": _minute(event), "events": 0, "passes": 0, "shot": False, "turnover": False}
        current["events"] += 1
        current["end_minute"] = _minute(event)
        if event_type == "Pass":
            current["passes"] += 1
        if event_type == "Shot":
            current["shot"] = True
        if _is_turnover(event):
            current["turnover"] = True
            chains.append(current)
            current = None
    if current:
        chains.append(current)

    by_team: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for chain in chains:
        by_team[chain["team"]].append(chain)

    summary: dict[str, dict[str, float]] = {}
    for team, team_chains in by_team.items():
        total = len(team_chains)
        lengths = [chain["events"] for chain in team_chains]
        passes = [chain["passes"] for chain in team_chains]
        summary[team] = {
            "Average Chain Length": round(sum(lengths) / total, 1) if total else 0.0,
            "Longest Chain": max(lengths, default=0),
            "Average Passes": round(sum(passes) / total, 1) if total else 0.0,
            "Chains Ending in Shot": sum(1 for chain in team_chains if chain["shot"]),
            "Chains Ending in Turnover": sum(1 for chain in team_chains if chain["turnover"]),
        }
    return {"chains": chains, "summary": summary}


def calculate_pressing_analysis(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate high/mid/low pressing volumes, timeline, and success."""
    teams = _teams(events or [])
    zones = {team: {"High Press": 0, "Mid Block": 0, "Low Block": 0} for team in teams}
    max_minute = max((_minute(event) for event in events or []), default=0)
    timeline = {team: [0 for _ in range(max_minute + 1)] for team in teams}
    pressures = {team: 0 for team in teams}
    pressure_success = {team: 0 for team in teams}
    sorted_events = sorted(enumerate(events or []), key=lambda item: (_period(item[1]), _minute(item[1]), _second(item[1]), item[0]))

    for index, (_, event) in enumerate(sorted_events):
        team = _team(event)
        if not team or _event_type(event) != "Pressure":
            continue
        loc = _location(event)
        x = loc[0] if loc else 0.0
        zone = "High Press" if x >= 80 else "Mid Block" if x >= 40 else "Low Block"
        zones[team][zone] += 1
        timeline[team][_minute(event)] += 1
        pressures[team] += 1
        for _, next_event in sorted_events[index + 1 : index + 6]:
            if _team(next_event) == team and _event_type(next_event) in {"Ball Recovery", "Interception"}:
                pressure_success[team] += 1
                break

    success_rates = {
        team: round((pressure_success.get(team, 0) / pressures.get(team, 0) * 100.0) if pressures.get(team, 0) else 0.0, 1)
        for team in teams
    }
    return {"zones": zones, "minutes": list(range(max_minute + 1)), "timeline": timeline, "success": success_rates}


def calculate_zone_dominance(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Calculate team action-share percentages by pitch lanes and thirds."""
    counts = _empty_team_counts(events or [])
    labels = [
        "Left Wing",
        "Left Half Space",
        "Centre",
        "Right Half Space",
        "Right Wing",
        "Defensive Third",
        "Middle Third",
        "Attacking Third",
    ]
    for event in events or []:
        team = _team(event)
        loc = _location(event)
        if not team or not loc:
            continue
        counts[team]["lane_total"] += 1
        counts[team]["third_total"] += 1
        counts[team][_vertical_lane(loc[1])] += 1
        counts[team][_third(loc[0])] += 1

    result: dict[str, dict[str, float]] = {}
    for team, values in counts.items():
        lane_total = values.get("lane_total", 0.0)
        third_total = values.get("third_total", 0.0)
        result[team] = {}
        for label in labels[:5]:
            result[team][label] = round((values.get(label, 0.0) / lane_total * 100.0) if lane_total else 0.0, 1)
        for label in labels[5:]:
            result[team][label] = round((values.get(label, 0.0) / third_total * 100.0) if third_total else 0.0, 1)
    return result


def calculate_expected_threat(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate deterministic expected threat from pitch-zone value changes."""
    team_xt: dict[str, float] = defaultdict(float)
    player_xt: dict[str, float] = defaultdict(float)
    actions: list[dict[str, Any]] = []
    for event in events or []:
        team = _team(event)
        if not team:
            continue
        xt = _xt_added(event)
        if xt <= 0:
            continue
        player = _player(event)
        team_xt[team] += xt
        player_xt[player] += xt
        actions.append(
            {
                "team": team,
                "player": player,
                "action": _event_type(event),
                "minute": _minute(event),
                "xT": round(xt, 4),
            }
        )
    return {
        "teams": sorted(({"team": team, "xT": round(value, 3)} for team, value in team_xt.items()), key=lambda item: item["xT"], reverse=True),
        "players": sorted(({"player": player, "xT": round(value, 3)} for player, value in player_xt.items()), key=lambda item: item["xT"], reverse=True)[:10],
        "actions": sorted(actions, key=lambda item: item["xT"], reverse=True)[:15],
    }


def calculate_team_similarity(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare teams across normalized tactical dimensions."""
    kpis = calculate_team_kpis(events)
    stats = calculate_team_statistics(events)
    metrics = ["Possession", "Passing", "Progression", "Pressing", "Recoveries", "Expected Threat", "Shot Creation"]
    raw: dict[str, dict[str, float]] = {}
    for team, values in kpis.items():
        team_stats = stats.get(team, {})
        raw[team] = {
            "Possession": values.get("Possession %", 0.0),
            "Passing": values.get("Pass Accuracy", 0.0),
            "Progression": values.get("Progressive Passes", 0.0) + values.get("Progressive Carries", 0.0),
            "Pressing": values.get("Pressures", 0.0),
            "Recoveries": values.get("Recoveries", 0.0),
            "Expected Threat": values.get("Expected Threat", 0.0),
            "Shot Creation": team_stats.get("shots", 0.0),
        }
    normalized: dict[str, dict[str, float]] = {team: {} for team in raw}
    for metric in metrics:
        max_value = max((team_values.get(metric, 0.0) for team_values in raw.values()), default=0.0)
        for team, team_values in raw.items():
            normalized[team][metric] = round((team_values.get(metric, 0.0) / max_value * 100.0) if max_value else 0.0, 1)
    return {"metrics": metrics, "raw": raw, "normalized": normalized}


def generate_team_summary(events: list[dict[str, Any]]) -> list[str]:
    """Generate deterministic team-level football insights."""
    kpis = calculate_team_kpis(events)
    styles = detect_playing_style(events)
    zones = calculate_zone_dominance(events)
    xt = calculate_expected_threat(events)
    xt_by_team = {item["team"]: item["xT"] for item in xt.get("teams", [])}
    summaries: list[str] = []
    for team, values in kpis.items():
        style = styles.get(team, "Balanced").lower()
        zone_values = zones.get(team, {})
        dominant_zone = max(zone_values, key=zone_values.get) if zone_values else "central zones"
        summaries.append(
            f"{team} profiled as {style}, with {values.get('Possession %', 0.0)}% possession, "
            f"{values.get('Progressive Passes', 0)} progressive passes and most activity through {dominant_zone}."
        )
        if values.get("Pressures", 0) >= 30:
            summaries.append(f"{team} applied sustained pressure, recording {values.get('Pressures', 0)} pressures and {values.get('Recoveries', 0)} recoveries.")
        if xt_by_team.get(team, 0.0) > 0:
            summaries.append(f"{team} generated {xt_by_team.get(team, 0.0)} expected threat from deterministic pitch-zone value gains.")
    if len(xt.get("teams", [])) >= 2:
        leader = xt["teams"][0]
        summaries.append(f"{leader['team']} generated the stronger expected-threat profile at {leader['xT']} xT.")
    return summaries or ["No team intelligence insights are available for this match event set."]
