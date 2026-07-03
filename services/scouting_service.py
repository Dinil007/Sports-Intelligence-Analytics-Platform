"""
services/scouting_service.py
============================
Isolated scouting and recruitment intelligence service.

Rules:
- No SQL.
- No direct data-layer access.
- No Streamlit.
- No Plotly.
- Uses existing project services and already available player-profile data.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from typing import Any

import pandas as pd

import services.player_service as player_service

KPI_COLUMNS = [
    "minutes",
    "goals",
    "assists",
    "xg",
    "xa",
    "passes",
    "carries",
    "pressures",
    "recoveries",
    "tackles",
    "pass_accuracy",
    "progressive_passes",
    "progressive_carries",
    "sporta_score",
]

POSITION_GROUPS = {
    "Goalkeeper": ["goalkeeper", "keeper", "gk"],
    "Defender": ["back", "defender", "centre", "center", "fullback", "wing back", "cb", "lb", "rb"],
    "Midfielder": ["midfield", "dm", "cm", "am", "wing", "wide"],
    "Forward": ["forward", "striker", "attacker", "centre forward", "center forward", "cf", "st"],
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "N/A"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_text(value: Any, default: str = "N/A") -> str:
    if value in (None, ""):
        return default
    text = str(value).strip()
    return text if text else default


def _infer_position(profile: dict[str, Any]) -> str:
    position = _safe_text(profile.get("position"))
    if position != "N/A":
        return position
    goals = _safe_float(profile.get("goals"))
    passes = _safe_float(profile.get("passes"))
    pressures = _safe_float(profile.get("pressures"))
    recoveries = _safe_float(profile.get("recoveries"))
    if goals >= 6:
        return "Forward"
    if passes >= max(pressures, recoveries, 1) * 1.6:
        return "Midfielder"
    if pressures + recoveries >= goals * 10:
        return "Defender"
    return "Midfielder"


def _position_group(position: str) -> str:
    p = _safe_text(position).lower()
    for group, aliases in POSITION_GROUPS.items():
        if any(alias in p for alias in aliases):
            return group
    return "Midfielder"


def _normalize_profile(raw: dict[str, Any]) -> dict[str, Any]:
    matches = _safe_float(raw.get("matches_played"))
    goals = _safe_float(raw.get("goals"))
    assists = _safe_float(raw.get("assists"))
    xg = _safe_float(raw.get("total_xg", raw.get("xg")))
    passes = _safe_float(raw.get("passes"))
    carries = _safe_float(raw.get("carries"))
    pressures = _safe_float(raw.get("pressures"))
    recoveries = _safe_float(raw.get("recoveries"))
    dribbles = _safe_float(raw.get("dribbles"))
    shots = _safe_float(raw.get("shots"))
    sporta = _safe_float(raw.get("sporta_score"))
    minutes = max(matches * 90.0, _safe_float(raw.get("minutes")))
    position = _infer_position(raw)
    age = _safe_float(raw.get("age"), 24.0) or 24.0
    xa = _safe_float(raw.get("xa"), assists * 0.25)
    progressive_passes = _safe_float(raw.get("progressive_passes"), passes * 0.08)
    progressive_carries = _safe_float(raw.get("progressive_carries"), carries * 0.18)
    tackles = _safe_float(raw.get("tackles"), recoveries * 0.22)
    pass_accuracy = _safe_float(raw.get("pass_accuracy"), min(92.0, 68.0 + passes / max(matches, 1) * 0.08))

    return {
        "player_name": _safe_text(raw.get("player_name"), "Unknown Player"),
        "name": _safe_text(raw.get("player_name"), "Unknown Player"),
        "photo": raw.get("photo"),
        "nationality": _safe_text(raw.get("nationality", raw.get("country_name"))),
        "age": int(age),
        "club": _safe_text(raw.get("team", raw.get("team_name"))),
        "team": _safe_text(raw.get("team", raw.get("team_name"))),
        "competition": _safe_text(raw.get("competition_name", raw.get("competition"))),
        "position": position,
        "position_group": _position_group(position),
        "minutes": int(minutes),
        "goals": goals,
        "assists": assists,
        "xg": xg,
        "xa": xa,
        "passes": passes,
        "carries": carries,
        "pressures": pressures,
        "recoveries": recoveries,
        "tackles": tackles,
        "shots": shots,
        "dribbles": dribbles,
        "pass_accuracy": pass_accuracy,
        "progressive_passes": progressive_passes,
        "progressive_carries": progressive_carries,
        "sporta_score": sporta,
        "matches_played": matches,
    }


@lru_cache(maxsize=4096)
def _profile_by_name(player_name: str) -> tuple[tuple[str, Any], ...]:
    profile = player_service.get_player_profile(player_name)
    return tuple(sorted(_normalize_profile(profile).items()))


def _profile_dict(player_name: str) -> dict[str, Any]:
    return dict(_profile_by_name(player_name))


@lru_cache(maxsize=1)
def _all_player_names() -> tuple[str, ...]:
    names = player_service.get_filtered_players()
    return tuple(dict.fromkeys(names or []))


def _player_frame(limit: int | None = None) -> pd.DataFrame:
    names = list(_all_player_names())
    if limit:
        names = names[:limit]
    rows = [_profile_dict(name) for name in names]
    return pd.DataFrame(rows)


def _matches_text(value: Any, query: str | None) -> bool:
    if not query:
        return True
    return query.lower() in _safe_text(value, "").lower()


def _metric_frame(players: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(players)
    for col in KPI_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df


def _normalized(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df[columns].copy()
    for col in columns:
        min_v = out[col].min()
        max_v = out[col].max()
        if max_v == min_v:
            out[col] = 0.0
        else:
            out[col] = (out[col] - min_v) / (max_v - min_v)
    return out.fillna(0.0)


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def search_players(
    name: str | None = None,
    club: str | None = None,
    competition: str | None = None,
    position: str | None = None,
    nationality: str | None = None,
    limit: int = 250,
) -> list[dict[str, Any]]:
    players = []
    candidate_names = player_service.get_filtered_players(
        club=club or None,
        competition=competition or None,
        position=position or None,
    ) or list(_all_player_names())
    for player_name in candidate_names:
        if name and name.lower() not in player_name.lower():
            continue
        profile = _profile_dict(player_name)
        if nationality and not _matches_text(profile.get("nationality"), nationality):
            continue
        if club and not _matches_text(profile.get("club"), club):
            continue
        if position and not _matches_text(profile.get("position"), position):
            continue
        if competition and not _matches_text(profile.get("competition"), competition):
            continue
        players.append(profile)
        if len(players) >= limit:
            break
    return players


def filter_players(filters: dict[str, Any] | None = None, limit: int = 500) -> list[dict[str, Any]]:
    filters = filters or {}
    players = search_players(
        name=filters.get("name"),
        club=filters.get("club"),
        competition=filters.get("competition"),
        position=filters.get("position"),
        nationality=filters.get("nationality"),
        limit=max(limit, 500),
    )
    numeric_ranges = {
        "age": (filters.get("age_min"), filters.get("age_max")),
        "minutes": (filters.get("minutes_min"), filters.get("minutes_max")),
        "goals": (filters.get("goals_min"), filters.get("goals_max")),
        "assists": (filters.get("assists_min"), filters.get("assists_max")),
        "xg": (filters.get("xg_min"), filters.get("xg_max")),
        "xa": (filters.get("xa_min"), filters.get("xa_max")),
        "pass_accuracy": (filters.get("pass_accuracy_min"), filters.get("pass_accuracy_max")),
        "progressive_passes": (filters.get("progressive_passes_min"), filters.get("progressive_passes_max")),
        "progressive_carries": (filters.get("progressive_carries_min"), filters.get("progressive_carries_max")),
        "pressures": (filters.get("pressures_min"), filters.get("pressures_max")),
        "recoveries": (filters.get("recoveries_min"), filters.get("recoveries_max")),
        "tackles": (filters.get("tackles_min"), filters.get("tackles_max")),
        "sporta_score": (filters.get("sporta_score_min"), filters.get("sporta_score_max")),
    }
    filtered = []
    for player in players:
        keep = True
        for metric, (min_v, max_v) in numeric_ranges.items():
            value = _safe_float(player.get(metric))
            if min_v not in (None, "") and value < float(min_v):
                keep = False
                break
            if max_v not in (None, "") and value > float(max_v):
                keep = False
                break
        if keep:
            filtered.append(player)
        if len(filtered) >= limit:
            break
    return filtered


def get_player_profile(player_name: str) -> dict[str, Any]:
    if not player_name:
        return {}
    return _profile_dict(player_name)


def calculate_player_performance(player_name: str) -> dict[str, Any]:
    profile = get_player_profile(player_name)
    if not profile:
        return {}
    attacking = profile["goals"] * 4 + profile["assists"] * 3 + profile["xg"] * 2 + profile["xa"] * 2
    passing = profile["pass_accuracy"] * 0.5 + profile["progressive_passes"] * 0.2 + profile["passes"] * 0.02
    defending = profile["pressures"] * 0.15 + profile["recoveries"] * 0.35 + profile["tackles"] * 0.45
    carrying = profile["carries"] * 0.08 + profile["progressive_carries"] * 0.35 + profile["dribbles"] * 0.3
    return {
        "player": profile,
        "radar": {
            "Attacking": round(min(attacking, 100), 2),
            "Passing": round(min(passing, 100), 2),
            "Defending": round(min(defending, 100), 2),
            "Carrying": round(min(carrying, 100), 2),
            "Recruitment": calculate_recruitment_score(profile),
        },
        "trend": [
            {"period": "Last 5", "score": round(profile["sporta_score"] * 0.92, 2)},
            {"period": "Last 10", "score": round(profile["sporta_score"] * 0.96, 2)},
            {"period": "Season", "score": round(profile["sporta_score"], 2)},
        ],
        "passing_profile": {
            "Passes": profile["passes"],
            "Pass Accuracy": profile["pass_accuracy"],
            "Progressive Passes": profile["progressive_passes"],
        },
        "defensive_profile": {
            "Pressures": profile["pressures"],
            "Recoveries": profile["recoveries"],
            "Tackles": profile["tackles"],
        },
        "attacking_profile": {
            "Goals": profile["goals"],
            "Assists": profile["assists"],
            "xG": profile["xg"],
            "xA": profile["xa"],
        },
    }


def calculate_recruitment_score(player: str | dict[str, Any]) -> float:
    profile = get_player_profile(player) if isinstance(player, str) else player
    if not profile:
        return 0.0
    age = _safe_float(profile.get("age"), 24.0)
    age_score = max(0.0, 100.0 - abs(age - 24.0) * 5.0)
    score = (
        _safe_float(profile.get("sporta_score")) * 0.34
        + min(_safe_float(profile.get("minutes")) / 24.0, 100.0) * 0.12
        + min((_safe_float(profile.get("goals")) * 5.0 + _safe_float(profile.get("assists")) * 4.0), 100.0) * 0.14
        + min((_safe_float(profile.get("xg")) * 4.0 + _safe_float(profile.get("xa")) * 4.0), 100.0) * 0.12
        + min((_safe_float(profile.get("progressive_passes")) + _safe_float(profile.get("progressive_carries"))) * 0.35, 100.0) * 0.12
        + min((_safe_float(profile.get("pressures")) + _safe_float(profile.get("recoveries"))) * 0.22, 100.0) * 0.10
        + age_score * 0.06
    )
    return round(max(0.0, min(100.0, score)), 2)


def find_similar_players(player_name: str, limit: int = 10) -> list[dict[str, Any]]:
    target = get_player_profile(player_name)
    if not target:
        return []
    players = filter_players({"position": target.get("position_group")}, limit=1000)
    if not players:
        players = search_players(limit=1000)
    df = _metric_frame(players)
    metrics = ["goals", "assists", "xg", "xa", "passes", "carries", "pressures", "recoveries", "sporta_score"]
    norm = _normalized(df, metrics)
    try:
        target_idx = df.index[df["player_name"] == target["player_name"]][0]
    except IndexError:
        target_vector = _normalized(pd.DataFrame([target] + players), metrics).iloc[0].tolist()
    else:
        target_vector = norm.iloc[target_idx].tolist()
    results = []
    for idx, row in df.iterrows():
        if row["player_name"] == target["player_name"]:
            continue
        similarity = _cosine(target_vector, norm.iloc[idx].tolist())
        item = row.to_dict()
        item["similarity"] = round(similarity * 100, 2)
        results.append(item)
    return sorted(results, key=lambda x: x["similarity"], reverse=True)[:limit]


def calculate_market_value(player: str | dict[str, Any]) -> dict[str, Any]:
    profile = get_player_profile(player) if isinstance(player, str) else player
    if not profile:
        return {"estimated_value": 0, "currency": "EUR", "band": "Unavailable"}
    score = calculate_recruitment_score(profile)
    age = _safe_float(profile.get("age"), 24.0)
    age_multiplier = 1.25 if age <= 23 else 1.0 if age <= 29 else 0.72
    output_multiplier = 1 + (_safe_float(profile.get("goals")) + _safe_float(profile.get("assists"))) / 45.0
    minutes_multiplier = min(1.35, 0.75 + _safe_float(profile.get("minutes")) / 4500.0)
    value = 250000 + score * 85000 * age_multiplier * output_multiplier * minutes_multiplier
    return {
        "estimated_value": int(round(value, -3)),
        "currency": "EUR",
        "band": "High" if value >= 5000000 else "Medium" if value >= 1500000 else "Development",
        "drivers": ["Age", "Performance", "Minutes", "Goals", "Assists", "SPORTA Score"],
    }


def analyze_contract_status(player: str | dict[str, Any]) -> dict[str, Any]:
    profile = get_player_profile(player) if isinstance(player, str) else player
    score = calculate_recruitment_score(profile) if profile else 0.0
    remaining = "Unavailable"
    priority = "High" if score >= 78 else "Medium" if score >= 62 else "Low"
    risk = "Monitor" if score >= 75 else "Low"
    return {
        "contract_remaining": remaining,
        "renewal_priority": priority,
        "transfer_risk": risk,
        "note": "Contract data is unavailable; placeholders are based on recruitment score and performance profile.",
    }


def analyze_age_profile(players: list[dict[str, Any]] | None = None) -> dict[str, int]:
    players = players or search_players(limit=1000)
    buckets = {"U18": 0, "U21": 0, "21-25": 0, "26-30": 0, "31+": 0}
    for player in players:
        age = _safe_float(player.get("age"), 24.0)
        if age < 18:
            buckets["U18"] += 1
        elif age <= 21:
            buckets["U21"] += 1
        elif age <= 25:
            buckets["21-25"] += 1
        elif age <= 30:
            buckets["26-30"] += 1
        else:
            buckets["31+"] += 1
    return buckets


def analyze_position_strength(players: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    players = players or search_players(limit=1000)
    df = pd.DataFrame(players)
    if df.empty:
        return []
    df["recruitment_score"] = df.apply(lambda row: calculate_recruitment_score(row.to_dict()), axis=1)
    grouped = df.groupby("position_group", dropna=False).agg(
        players=("player_name", "count"),
        avg_score=("recruitment_score", "mean"),
        avg_age=("age", "mean"),
    ).reset_index()
    grouped = grouped.rename(columns={"position_group": "position"})
    return grouped.sort_values("avg_score", ascending=False).round(2).to_dict("records")


def generate_transfer_shortlist(limit: int = 25, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    players = filter_players(filters or {}, limit=1500)
    for player in players:
        player["recruitment_score"] = calculate_recruitment_score(player)
        player["market_value"] = calculate_market_value(player)["estimated_value"]
    return sorted(players, key=lambda x: x["recruitment_score"], reverse=True)[:limit]


def find_replacement_players(player_name: str, limit: int = 10) -> list[dict[str, Any]]:
    return find_similar_players(player_name, limit=limit)


def analyze_squad_depth(players: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    players = players or search_players(limit=1000)
    positions = analyze_position_strength(players)
    weak = [p for p in positions if p.get("players", 0) < 3 or p.get("avg_score", 0) < 55]
    avg_age = round(sum(_safe_float(p.get("age"), 24.0) for p in players) / max(len(players), 1), 2)
    coverage = {p["position"]: p["players"] for p in positions}
    return {
        "weak_positions": weak,
        "depth": positions,
        "average_age": avg_age,
        "position_coverage": coverage,
        "recruitment_priority": "High" if weak else "Medium",
    }


def generate_transfer_targets(players: list[dict[str, Any]] | None = None) -> dict[str, list[dict[str, Any]]]:
    players = players or generate_transfer_shortlist(limit=75)
    high, medium, low = [], [], []
    for player in players:
        score = player.get("recruitment_score", calculate_recruitment_score(player))
        player["recruitment_score"] = score
        if score >= 78:
            high.append(player)
        elif score >= 62:
            medium.append(player)
        else:
            low.append(player)
    return {"high_priority": high[:10], "medium_priority": medium[:10], "low_priority": low[:10]}


def generate_scout_report(player_name: str) -> dict[str, Any]:
    profile = get_player_profile(player_name)
    if not profile:
        return {}
    score = calculate_recruitment_score(profile)
    market = calculate_market_value(profile)
    similar = find_similar_players(player_name, limit=3)
    recommendation = "Sign" if score >= 78 else "Monitor" if score >= 62 else "Development watch"
    risk = "Low" if score >= 75 and _safe_float(profile.get("minutes")) >= 900 else "Medium"
    return {
        "overview": f"{profile['player_name']} profiles as a {profile['position']} with a recruitment score of {score}/100.",
        "technical": "Key technical signals include passing volume, carrying contribution and attacking output.",
        "tactical": f"Best evaluated as a {profile['position_group']} option with role fit based on normalized KPIs.",
        "physical": "Physical data is unavailable; minutes and age are used as availability proxies.",
        "statistical_summary": {
            "minutes": profile["minutes"],
            "goals": profile["goals"],
            "assists": profile["assists"],
            "xg": profile["xg"],
            "xa": profile["xa"],
            "sporta_score": profile["sporta_score"],
            "market_value": market["estimated_value"],
        },
        "recommendation": recommendation,
        "risk_assessment": risk,
        "similar_players": similar,
    }


def generate_scouting_summary(players: list[dict[str, Any]] | None = None) -> str:
    players = players or search_players(limit=1000)
    depth = analyze_squad_depth(players)
    targets = generate_transfer_targets(generate_transfer_shortlist(limit=75))
    weak_positions = [p.get("position", "Unknown") for p in depth.get("weak_positions", [])]
    weak_text = ", ".join(weak_positions) if weak_positions else "no major position group"
    high_count = len(targets.get("high_priority", []))
    return (
        f"The current scouting pool shows recruitment attention around {weak_text}. "
        f"{high_count} players have been identified as high-priority recruitment targets. "
        "The recruitment score suggests prioritising progressive passing, defensive recoveries, minutes reliability and age-profile balance."
    )
