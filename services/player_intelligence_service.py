"""
services/player_intelligence_service.py
======================================
Deterministic Player Intelligence & Performance Analytics calculations.

No SQL. No repositories. No ML. No AI. All functions consume the events list
provided by get_match_dashboard()["events"].
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

PROGRESSIVE_GAIN = 10.0
RADAR_METRICS = [
    "passes",
    "shots",
    "carries",
    "pressures",
    "recoveries",
    "tackles",
    "progressive_passes",
    "progressive_carries",
]


def _player_name(event: dict[str, Any]) -> str | None:
    player = event.get("player_name")
    if not player:
        return None
    name = str(player).strip()
    return name or None


def _team_name(event: dict[str, Any]) -> str:
    team = event.get("team_name")
    return str(team).strip() if team else "Unknown"


def _minute(event: dict[str, Any]) -> int:
    try:
        minute = int(event.get("minute") or 0)
    except (TypeError, ValueError):
        minute = 0
    return max(0, minute)


def _second(event: dict[str, Any]) -> int:
    try:
        second = int(event.get("second") or 0)
    except (TypeError, ValueError):
        second = 0
    return max(0, second)


def _location(event: dict[str, Any], key: str = "location") -> list[float] | None:
    loc = event.get(key)
    if isinstance(loc, (list, tuple)) and len(loc) >= 2:
        try:
            return [float(loc[0]), float(loc[1])]
        except (TypeError, ValueError):
            return None
    return None


def _end_location(event: dict[str, Any]) -> list[float] | None:
    if event.get("event_type") == "Pass":
        return _location(event, "pass_end_location")
    if event.get("event_type") == "Carry":
        return _location(event, "carry_end_location")
    return _location(event, "pass_end_location") or _location(event, "carry_end_location")


def _forward_gain(event: dict[str, Any]) -> float:
    start = _location(event)
    end = _end_location(event)
    if not start or not end:
        return 0.0
    return max(0.0, end[0] - start[0])


def _is_progressive_pass(event: dict[str, Any]) -> bool:
    return event.get("event_type") == "Pass" and _forward_gain(event) >= PROGRESSIVE_GAIN


def _is_progressive_carry(event: dict[str, Any]) -> bool:
    return event.get("event_type") == "Carry" and _forward_gain(event) >= PROGRESSIVE_GAIN


def _is_recovery(event: dict[str, Any]) -> bool:
    return event.get("event_type") in {"Ball Recovery", "Interception"}


def _is_tackle(event: dict[str, Any]) -> bool:
    event_type = event.get("event_type")
    if event_type == "Tackle":
        return True
    if event_type != "Duel":
        return False
    values = [event.get("duel_type"), event.get("duel_outcome"), event.get("outcome"), event.get("result")]
    return any("tackle" in str(value).lower() or "won" in str(value).lower() for value in values if value is not None)


def _is_goal(event: dict[str, Any]) -> bool:
    values = [event.get("shot_outcome"), event.get("outcome"), event.get("result")]
    return event.get("event_type") == "Shot" and any(str(value).lower() == "goal" for value in values if value is not None)


def _is_assist(event: dict[str, Any]) -> bool:
    values = [event.get("pass_goal_assist"), event.get("assist"), event.get("is_assist")]
    return any(value is True or str(value).lower() in {"true", "1", "assist"} for value in values if value is not None)


def _empty_stats(player: str, team: str) -> dict[str, Any]:
    return {
        "player": player,
        "team": team,
        "events": 0,
        "passes": 0,
        "shots": 0,
        "carries": 0,
        "pressures": 0,
        "recoveries": 0,
        "tackles": 0,
        "goals": 0,
        "assists": 0,
        "progressive_passes": 0,
        "progressive_carries": 0,
        "touches": 0,
        "attacking_actions": 0,
        "progressive_actions": 0,
        "score_raw": 0.0,
    }


def calculate_player_statistics(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Aggregate deterministic player event statistics."""
    stats: dict[str, dict[str, Any]] = {}
    for event in events:
        player = _player_name(event)
        if not player:
            continue
        team = _team_name(event)
        if player not in stats:
            stats[player] = _empty_stats(player, team)
        row = stats[player]
        row["team"] = row.get("team") or team
        row["events"] += 1

        event_type = event.get("event_type")
        if event_type == "Pass":
            row["passes"] += 1
            row["score_raw"] += 1.0
            if _is_progressive_pass(event):
                row["progressive_passes"] += 1
                row["progressive_actions"] += 1
                row["score_raw"] += 1.5
        elif event_type == "Shot":
            row["shots"] += 1
            row["attacking_actions"] += 1
            row["score_raw"] += 2.0
            if _is_goal(event):
                row["goals"] += 1
                row["score_raw"] += 10.0
        elif event_type == "Carry":
            row["carries"] += 1
            row["score_raw"] += 1.0
            if _is_progressive_carry(event):
                row["progressive_carries"] += 1
                row["progressive_actions"] += 1
                row["score_raw"] += 1.5
        elif event_type == "Pressure":
            row["pressures"] += 1
            row["score_raw"] += 1.0

        if _is_recovery(event):
            row["recoveries"] += 1
            row["score_raw"] += 2.0
        if _is_tackle(event):
            row["tackles"] += 1
            row["score_raw"] += 2.0
        if _is_assist(event):
            row["assists"] += 1
            row["score_raw"] += 8.0

        if _location(event):
            row["touches"] += 1

    return stats


def calculate_player_scores(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Calculate normalized 0-10 player performance scores."""
    stats = calculate_player_statistics(events)
    max_raw = max((row["score_raw"] for row in stats.values()), default=0.0)
    scores: dict[str, dict[str, Any]] = {}
    for player, row in stats.items():
        score = (row["score_raw"] / max_raw * 10.0) if max_raw else 0.0
        scores[player] = {
            "player": player,
            "team": row["team"],
            "score": round(score, 2),
            "stars": max(0, min(5, round(score / 2))),
            "raw_score": round(row["score_raw"], 2),
        }
    return scores


def calculate_player_rankings(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return top players sorted by normalized performance score."""
    stats = calculate_player_statistics(events)
    scores = calculate_player_scores(events)
    rows: list[dict[str, Any]] = []
    for player, row in stats.items():
        score = scores.get(player, {}).get("score", 0.0)
        rows.append({
            "player": player,
            "team": row["team"],
            "score": score,
            "passes": row["passes"],
            "shots": row["shots"],
            "carries": row["carries"],
            "recoveries": row["recoveries"],
        })
    return sorted(rows, key=lambda item: item["score"], reverse=True)


def calculate_player_radar(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Return radar metrics by player."""
    stats = calculate_player_statistics(events)
    return {
        player: {"team": row["team"], **{metric: row.get(metric, 0) for metric in RADAR_METRICS}}
        for player, row in stats.items()
    }


def calculate_player_influence(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Return player touch coordinates for pitch influence maps."""
    influence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        player = _player_name(event)
        loc = _location(event)
        if not player or not loc:
            continue
        influence[player].append({
            "x": loc[0],
            "y": loc[1],
            "minute": _minute(event),
            "event_type": event.get("event_type") or "Event",
            "team": _team_name(event),
        })
    return dict(influence)


def calculate_player_timeline(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Return cumulative player events by minute for key event types."""
    max_minute = max((_minute(event) for event in events), default=0)
    minutes = list(range(max_minute + 1))
    metrics = {
        "Passes": "Pass",
        "Carries": "Carry",
        "Pressures": "Pressure",
        "Recoveries": "Ball Recovery",
    }
    players = sorted({_player_name(event) for event in events if _player_name(event)})
    timeline: dict[str, dict[str, list[int]]] = {
        player: {metric: [0 for _ in minutes] for metric in metrics} for player in players
    }

    for event in events:
        player = _player_name(event)
        if not player or player not in timeline:
            continue
        minute = _minute(event)
        event_type = event.get("event_type")
        for metric, expected_type in metrics.items():
            if event_type == expected_type or (metric == "Recoveries" and _is_recovery(event)):
                timeline[player][metric][minute] += 1

    for player_metrics in timeline.values():
        for metric, values in player_metrics.items():
            running = 0
            cumulative = []
            for value in values:
                running += value
                cumulative.append(running)
            player_metrics[metric] = cumulative

    return {"minutes": minutes, "players": timeline}


def detect_player_roles(events: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    """Detect deterministic football roles from player event profiles."""
    stats = calculate_player_statistics(events)
    roles: dict[str, dict[str, str]] = {}
    for player, row in stats.items():
        role = "All-Round Contributor"
        if row["shots"] >= max(3, row["passes"] * 0.08):
            role = "Forward"
        elif row["pressures"] + row["tackles"] >= max(6, row["passes"] * 0.35):
            role = "Ball Winning Midfielder"
        elif row["carries"] + row["progressive_actions"] >= max(8, row["passes"] * 0.35):
            role = "Box-to-Box Midfielder"
        elif row["recoveries"] >= max(4, row["pressures"] * 0.6):
            role = "Defensive Midfielder"
        elif row["passes"] >= 20 and row["shots"] <= 2:
            role = "Deep Lying Playmaker"
        roles[player] = {"player": player, "team": row["team"], "role": role}
    return roles


def generate_player_awards(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Generate deterministic match awards."""
    stats = calculate_player_statistics(events)
    scores = calculate_player_scores(events)
    if not stats:
        return {}

    def best_by(metric: str) -> str:
        return max(stats, key=lambda player: stats[player].get(metric, 0))

    def award(player: str, metric: str, value: Any) -> dict[str, Any]:
        return {"player": player, "team": stats[player]["team"], "metric": metric, "value": value}

    player_of_match = max(scores, key=lambda player: scores[player].get("score", 0.0)) if scores else best_by("events")
    best_passer = best_by("passes")
    best_defender = max(stats, key=lambda player: stats[player].get("recoveries", 0) + stats[player].get("tackles", 0))
    best_progressor = max(stats, key=lambda player: stats[player].get("progressive_passes", 0) + stats[player].get("progressive_carries", 0))
    creative = max(stats, key=lambda player: stats[player].get("shots", 0) + stats[player].get("progressive_passes", 0) + stats[player].get("assists", 0))
    presser = best_by("pressures")

    return {
        "Player of the Match": award(player_of_match, "Score", scores.get(player_of_match, {}).get("score", 0.0)),
        "Best Passer": award(best_passer, "Passes", stats[best_passer]["passes"]),
        "Best Defender": award(best_defender, "Defensive Actions", stats[best_defender]["recoveries"] + stats[best_defender]["tackles"]),
        "Best Ball Progressor": award(best_progressor, "Progressive Actions", stats[best_progressor]["progressive_passes"] + stats[best_progressor]["progressive_carries"]),
        "Most Creative Player": award(creative, "Creative Actions", stats[creative]["shots"] + stats[creative]["progressive_passes"] + stats[creative]["assists"]),
        "Best Presser": award(presser, "Pressures", stats[presser]["pressures"]),
    }


def generate_player_summary(events: list[dict[str, Any]]) -> str:
    """Generate a concise deterministic player performance summary."""
    rankings = calculate_player_rankings(events)
    stats = calculate_player_statistics(events)
    if not rankings:
        return "No player event data is available for player intelligence analysis."

    top = rankings[0]
    passer = max(stats, key=lambda player: stats[player].get("passes", 0))
    defender = max(stats, key=lambda player: stats[player].get("recoveries", 0) + stats[player].get("tackles", 0))
    creator = max(stats, key=lambda player: stats[player].get("progressive_passes", 0) + stats[player].get("shots", 0))

    return (
        f"{top['player']} delivered the strongest overall performance with a score of {top['score']}. "
        f"{passer} helped control possession through high passing volume. "
        f"{creator} contributed the most attacking progression and creative actions. "
        f"{defender} stood out in defensive transitions through recoveries and tackles."
    )


__all__ = [
    "calculate_player_statistics",
    "calculate_player_scores",
    "calculate_player_rankings",
    "calculate_player_radar",
    "calculate_player_influence",
    "calculate_player_timeline",
    "detect_player_roles",
    "generate_player_awards",
    "generate_player_summary",
]
