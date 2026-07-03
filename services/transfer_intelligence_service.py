"""Deterministic Transfer Intelligence calculations.

This module is intentionally isolated from presentation, storage, pipeline,
model, and assistant integrations. It consumes existing player dashboard
service data when available and falls back to empty structures.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from math import sqrt
from typing import Any


PositionGroup = str
PlayerRow = dict[str, Any]

POSITION_GROUPS: dict[PositionGroup, tuple[str, ...]] = {
    "Goalkeepers": ("goalkeeper", "keeper", "gk"),
    "Defenders": ("defender", "back", "centre-back", "center-back", "fullback", "wing-back", "cb", "lb", "rb"),
    "Midfielders": ("midfielder", "midfield", "cm", "dm", "am"),
    "Forwards": ("forward", "striker", "winger", "attacker", "cf", "st", "lw", "rw"),
}

METRIC_KEYS = ("goals", "assists", "xg", "xa", "passes", "carries", "pressures", "recoveries")


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "N/A"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_text(value: Any, default: str = "Unknown") -> str:
    if value in (None, ""):
        return default
    text = str(value).strip()
    return text if text else default


def _position_group(position: Any) -> str:
    position_text = _safe_text(position, "Midfielder").lower()
    for group, aliases in POSITION_GROUPS.items():
        if any(alias in position_text for alias in aliases):
            return group
    return "Midfielders"


def _priority(score: float, value: float) -> str:
    if score >= 78 and value <= 8_000_000:
        return "High"
    if score >= 64:
        return "Medium"
    return "Low"


def _contract_status(age: float, score: float) -> str:
    if age <= 23 and score >= 70:
        return "High resale window"
    if age >= 30:
        return "Short-term profile"
    if score >= 78:
        return "Prime target"
    return "Monitor"


def _sporta_score(player: PlayerRow) -> float:
    explicit = _safe_float(player.get("sporta_score"), -1.0)
    if explicit >= 0:
        return round(max(0.0, min(100.0, explicit)), 2)
    attacking = _safe_float(player.get("goals")) * 5.0 + _safe_float(player.get("assists")) * 4.0
    creation = _safe_float(player.get("xg")) * 8.0 + _safe_float(player.get("xa")) * 8.0
    possession = _safe_float(player.get("passes")) * 0.025 + _safe_float(player.get("carries")) * 0.04
    defensive = _safe_float(player.get("pressures")) * 0.08 + _safe_float(player.get("recoveries")) * 0.14
    return round(max(0.0, min(100.0, attacking + creation + possession + defensive)), 2)


def _market_value(player: PlayerRow) -> int:
    score = _sporta_score(player)
    age = _safe_float(player.get("age"), 24.0)
    minutes = _safe_float(player.get("minutes"), _safe_float(player.get("minutes_played"), 1_800.0))
    output = _safe_float(player.get("goals")) + _safe_float(player.get("assists"))
    age_multiplier = 1.28 if age <= 23 else 1.0 if age <= 29 else 0.68
    minutes_multiplier = min(1.35, 0.7 + minutes / 4_500.0)
    output_multiplier = 1.0 + min(output, 35.0) / 45.0
    value = 300_000 + score * 90_000 * age_multiplier * minutes_multiplier * output_multiplier
    return int(round(value, -3))


def _weekly_wage(value: float, score: float, age: float) -> int:
    wage = value * 0.0021 / 52.0 + score * 320.0
    if age >= 30:
        wage *= 1.08
    return int(round(max(5_000.0, wage), -2))


def _roi(value: float, score: float, age: float) -> float:
    resale = 1.18 if age <= 23 else 1.0 if age <= 28 else 0.72
    return round(((score * 120_000.0 * resale) - value) / max(value, 1.0) * 100.0, 2)


def _risk_bucket(value: float) -> str:
    if value >= 70:
        return "High"
    if value >= 38:
        return "Medium"
    return "Low"


def _normalise_player(player: PlayerRow) -> PlayerRow:
    name = _safe_text(player.get("player_name", player.get("name")), "Unknown Player")
    club = _safe_text(player.get("club", player.get("team")), "Unknown Club")
    position = _safe_text(player.get("position"), "Midfielder")
    age = _safe_float(player.get("age"), 24.0)
    score = _sporta_score(player)
    market_value = _market_value(player)
    wage = _weekly_wage(market_value, score, age)
    position_group = _position_group(position)
    normalised = dict(player)
    normalised.update(
        {
            "Player": name,
            "Club": club,
            "Position": position,
            "Position Group": position_group,
            "Age": round(age, 1),
            "SPORTA Score": score,
            "Market Value": market_value,
            "Contract Status": _contract_status(age, score),
            "Priority": _priority(score, market_value),
            "Weekly Wage": wage,
            "Transfer Cost": int(round(market_value * 1.08, -3)),
            "Performance Score": score,
            "ROI": _roi(market_value * 1.08, score, age),
        }
    )
    return normalised


def _empty_players() -> list[PlayerRow]:
    return []


@lru_cache(maxsize=1)
def _load_players() -> tuple[tuple[tuple[str, Any], ...], ...]:
    try:
        from services import player_service
    except Exception:
        return tuple()

    try:
        names = player_service.get_filtered_players() or []
    except Exception:
        return tuple()

    rows: list[PlayerRow] = []
    for name in list(dict.fromkeys(names))[:350]:
        try:
            profile = player_service.get_player_profile(name)
        except Exception:
            profile = {}
        if profile:
            rows.append(_normalise_player(profile))
    return tuple(tuple(sorted(row.items())) for row in rows)


def _players(players: list[PlayerRow] | None = None) -> list[PlayerRow]:
    if players is not None:
        return [_normalise_player(player) for player in players]
    cached = [dict(row) for row in _load_players()]
    return cached or _empty_players()


def calculate_transfer_targets(players: list[PlayerRow] | None = None) -> list[PlayerRow]:
    """Rank transfer targets by SPORTA score, ROI, age profile, and value."""
    rows = _players(players)
    for row in rows:
        value_score = max(0.0, 100.0 - row["Market Value"] / 150_000.0)
        row["Transfer Fit"] = round(row["SPORTA Score"] * 0.62 + max(row["ROI"], 0.0) * 0.18 + value_score * 0.2, 2)
    return sorted(rows, key=lambda item: item["Transfer Fit"], reverse=True)[:40]


def calculate_transfer_value(players: list[PlayerRow] | None = None) -> list[PlayerRow]:
    """Return market value versus SPORTA score rows for valuation analysis."""
    return calculate_transfer_targets(players)


def calculate_transfer_budget(players: list[PlayerRow] | None = None, available_budget: float = 75_000_000.0) -> dict[str, float]:
    """Calculate budget use from high-priority recommended targets."""
    targets = calculate_transfer_targets(players)
    selected = [target for target in targets if target["Priority"] == "High"][:5] or targets[:3]
    used = float(sum(target["Transfer Cost"] for target in selected))
    remaining = max(0.0, available_budget - used)
    return {
        "Available Budget": round(available_budget, 2),
        "Budget Used": round(min(used, available_budget), 2),
        "Remaining Budget": round(remaining, 2),
        "Budget Used %": round(min(100.0, used / available_budget * 100.0), 2) if available_budget else 0.0,
    }


def calculate_wage_structure(players: list[PlayerRow] | None = None) -> list[PlayerRow]:
    """Return projected wage structure for top transfer targets."""
    return sorted(calculate_transfer_targets(players), key=lambda item: item["Weekly Wage"], reverse=True)[:20]


def calculate_transfer_roi(players: list[PlayerRow] | None = None) -> list[PlayerRow]:
    """Return transfer cost, performance score, and ROI for target options."""
    return sorted(calculate_transfer_targets(players), key=lambda item: item["ROI"], reverse=True)[:30]


def _metric_vector(player: PlayerRow) -> list[float]:
    return [_safe_float(player.get(key)) for key in METRIC_KEYS]


def _distance(left: list[float], right: list[float]) -> float:
    return sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def calculate_replacement_options(players: list[PlayerRow] | None = None) -> dict[str, Any]:
    """Find the closest replacement profile for the highest-value current player."""
    rows = calculate_transfer_targets(players)
    if len(rows) < 2:
        return {"Current Player": None, "Replacement Player": None, "Metrics": list(METRIC_KEYS), "Current": [], "Replacement": []}

    current = max(rows, key=lambda item: item["SPORTA Score"])
    same_position = [row for row in rows if row["Player"] != current["Player"] and row["Position Group"] == current["Position Group"]]
    pool = same_position or [row for row in rows if row["Player"] != current["Player"]]
    current_vector = _metric_vector(current)
    replacement = min(pool, key=lambda item: _distance(current_vector, _metric_vector(item)))
    return {
        "Current Player": current["Player"],
        "Replacement Player": replacement["Player"],
        "Metrics": [key.replace("_", " ").title() for key in METRIC_KEYS],
        "Current": current_vector,
        "Replacement": _metric_vector(replacement),
    }


def calculate_squad_balance(players: list[PlayerRow] | None = None) -> list[dict[str, Any]]:
    """Calculate squad balance counts and ideal benchmark counts by position group."""
    rows = _players(players)
    counts = Counter(row["Position Group"] for row in rows)
    benchmark = {"Goalkeepers": 3, "Defenders": 8, "Midfielders": 8, "Forwards": 6}
    return [
        {"Position Group": group, "Current Squad": counts.get(group, 0), "Ideal Squad": benchmark[group]}
        for group in ("Goalkeepers", "Defenders", "Midfielders", "Forwards")
    ]


def calculate_transfer_priority(players: list[PlayerRow] | None = None) -> list[PlayerRow]:
    """Classify targets into impact-cost quadrants."""
    rows = calculate_transfer_targets(players)
    for row in rows:
        impact = "High Impact" if row["SPORTA Score"] >= 72 else "Low Impact"
        cost = "High Cost" if row["Market Value"] >= 8_000_000 else "Low Cost"
        row["Impact"] = impact
        row["Cost Band"] = cost
        row["Quadrant"] = f"{impact} / {cost}"
    return rows


def calculate_transfer_risk(players: list[PlayerRow] | None = None) -> list[dict[str, Any]]:
    """Calculate deterministic transfer risk scores for top targets."""
    risks: list[dict[str, Any]] = []
    for row in calculate_transfer_targets(players)[:15]:
        age = _safe_float(row.get("Age"), 24.0)
        score = _safe_float(row.get("SPORTA Score"))
        minutes = _safe_float(row.get("minutes"), _safe_float(row.get("minutes_played"), 1_800.0))
        age_risk = max(0.0, (age - 27.0) * 9.0) if age > 27 else max(0.0, (20.0 - age) * 5.0)
        injury_risk = max(8.0, min(82.0, 45.0 - minutes / 140.0 + max(age - 29.0, 0.0) * 4.0))
        contract_risk = 70.0 if row["Contract Status"] == "Prime target" else 44.0 if row["Contract Status"] == "Monitor" else 30.0
        adaptation_risk = max(12.0, 72.0 - score * 0.65)
        minutes_risk = max(5.0, min(85.0, 65.0 - minutes / 90.0))
        risks.append(
            {
                "Player": row["Player"],
                "Age Risk": round(age_risk, 1),
                "Injury Risk": round(injury_risk, 1),
                "Contract Risk": round(contract_risk, 1),
                "Adaptation Risk": round(adaptation_risk, 1),
                "Minutes Risk": round(minutes_risk, 1),
                "Overall Risk": _risk_bucket((age_risk + injury_risk + contract_risk + adaptation_risk + minutes_risk) / 5.0),
            }
        )
    return risks


def generate_transfer_summary(players: list[PlayerRow] | None = None) -> list[str]:
    """Generate deterministic football scouting summary from transfer KPIs."""
    targets = calculate_transfer_targets(players)
    budget = calculate_transfer_budget(players)
    risks = calculate_transfer_risk(players)
    balance = calculate_squad_balance(players)
    if not targets:
        return ["No transfer intelligence is available because no player dashboard data could be loaded."]

    top = targets[0]
    value_pick = max(targets, key=lambda item: item["ROI"])
    weakest_group = min(balance, key=lambda item: item["Current Squad"] - item["Ideal Squad"])
    high_risk_count = sum(1 for item in risks if item["Overall Risk"] == "High")
    return [
        f"{top['Player']} profiles as the leading target with a SPORTA Score of {top['SPORTA Score']} and a {top['Priority'].lower()} recruitment priority.",
        f"{value_pick['Player']} offers the strongest projected ROI at {value_pick['ROI']}% based on performance, cost, and age curve.",
        f"The planning model allocates EUR {budget['Budget Used']:,.0f} of EUR {budget['Available Budget']:,.0f}, leaving EUR {budget['Remaining Budget']:,.0f} for follow-up moves.",
        f"Squad balance points first toward {weakest_group['Position Group'].lower()}, where the current count is {weakest_group['Current Squad']} against an ideal benchmark of {weakest_group['Ideal Squad']}.",
        f"Risk screening flags {high_risk_count} high-risk targets among the priority list; contract, age, adaptation, injury, and minutes exposure should guide final due diligence.",
    ]

