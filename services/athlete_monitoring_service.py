"""Deterministic Athlete Monitoring and Performance Science calculations."""

from __future__ import annotations

from functools import lru_cache
from statistics import mean
from typing import Any


AthleteRow = dict[str, Any]

DATA_LABEL = "Demo-derived from existing player profile data; no GPS, heart-rate, or wellness feed is connected."


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


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _profile_score(profile: AthleteRow) -> float:
    explicit = _safe_float(profile.get("sporta_score"), -1.0)
    if explicit >= 0:
        return round(_clamp(explicit), 2)
    output = _safe_float(profile.get("goals")) * 4.0 + _safe_float(profile.get("assists")) * 3.0
    creation = _safe_float(profile.get("xg")) * 3.5 + _safe_float(profile.get("xa")) * 3.5
    possession = _safe_float(profile.get("passes")) * 0.025 + _safe_float(profile.get("carries")) * 0.035
    defensive = _safe_float(profile.get("pressures")) * 0.07 + _safe_float(profile.get("recoveries")) * 0.12
    return round(_clamp(output + creation + possession + defensive), 2)


def _normalise_profile(profile: AthleteRow) -> AthleteRow:
    minutes = _safe_float(profile.get("minutes"), _safe_float(profile.get("minutes_played"), 900.0))
    matches = max(1.0, _safe_float(profile.get("matches_played"), _safe_float(profile.get("matches"), 10.0)))
    age = _safe_float(profile.get("age"), 24.0)
    score = _profile_score(profile)
    actions = (
        _safe_float(profile.get("passes"))
        + _safe_float(profile.get("carries"))
        + _safe_float(profile.get("pressures"))
        + _safe_float(profile.get("recoveries"))
    )
    intensity = actions / max(minutes / 90.0, 1.0)
    sprint_count = max(1.0, _safe_float(profile.get("progressive_carries"), _safe_float(profile.get("carries")) * 0.18) / matches)
    high_intensity_runs = sprint_count + _safe_float(profile.get("pressures")) / matches * 0.35
    acute_load = _clamp(minutes / matches * 0.7 + intensity * 0.32, 10.0, 120.0)
    chronic_load = _clamp(minutes / matches * 0.62 + score * 0.42, 10.0, 120.0)
    fatigue = _clamp((acute_load / max(chronic_load, 1.0) - 0.8) * 70.0 + max(age - 29.0, 0.0) * 4.0 + high_intensity_runs * 0.8)
    recovery = _clamp(100.0 - fatigue * 0.55 + score * 0.12)
    wellness = _clamp(recovery * 0.58 + (100.0 - fatigue) * 0.28 + score * 0.14)
    readiness = _clamp(recovery * 0.45 + wellness * 0.35 + score * 0.2 - max(acute_load / max(chronic_load, 1.0) - 1.25, 0.0) * 20.0)
    avg_speed = 18.0 + score * 0.045 + sprint_count * 0.08
    max_speed = avg_speed + 4.2 + min(3.0, sprint_count * 0.06)
    total_distance = max(4.0, minutes / matches * 0.105 + intensity * 0.035)
    return {
        "Player": _safe_text(profile.get("player_name", profile.get("name")), "Unknown Player"),
        "Club": _safe_text(profile.get("club", profile.get("team")), "Unknown Club"),
        "Position": _safe_text(profile.get("position"), "Unknown"),
        "Age": round(age, 1),
        "SPORTA Score": score,
        "Minutes": round(minutes, 1),
        "Matches": int(matches),
        "Training Load": round(acute_load, 2),
        "Chronic Load": round(chronic_load, 2),
        "Fatigue Score": round(fatigue, 2),
        "Recovery Score": round(recovery, 2),
        "Wellness Score": round(wellness, 2),
        "Readiness Score": round(readiness, 2),
        "Average HR": round(118.0 + fatigue * 0.32 + acute_load * 0.08, 1),
        "Maximum HR": round(174.0 + fatigue * 0.12 + high_intensity_runs * 0.18, 1),
        "Recovery HR": round(62.0 + fatigue * 0.16 - recovery * 0.05, 1),
        "Total Distance": round(total_distance, 2),
        "Walking": round(total_distance * 0.24, 2),
        "Jogging": round(total_distance * 0.38, 2),
        "Running": round(total_distance * 0.27, 2),
        "Sprint Distance": round(total_distance * 0.11, 2),
        "Sprint Count": round(sprint_count, 1),
        "Maximum Speed": round(max_speed, 2),
        "Average Speed": round(avg_speed, 2),
        "High Intensity Runs": round(high_intensity_runs, 1),
    }


@lru_cache(maxsize=1)
def _load_athletes() -> tuple[tuple[tuple[str, Any], ...], ...]:
    try:
        from services import player_service
    except Exception:
        return tuple()

    try:
        names = player_service.get_filtered_players() or []
    except Exception:
        return tuple()

    rows: list[AthleteRow] = []
    for name in list(dict.fromkeys(names))[:500]:
        try:
            profile = player_service.get_player_profile(name)
        except Exception:
            profile = {}
        if profile:
            rows.append(_normalise_profile(profile))
    return tuple(tuple(sorted(row.items())) for row in rows)


def _athletes(athletes: list[AthleteRow] | None = None) -> list[AthleteRow]:
    if athletes is not None:
        return [_normalise_profile(athlete) for athlete in athletes]
    return [dict(row) for row in _load_athletes()]


def _primary_athlete(athletes: list[AthleteRow] | None = None) -> AthleteRow:
    rows = _athletes(athletes)
    if not rows:
        return {}
    return max(rows, key=lambda row: row.get("Minutes", 0.0))


def _series(base: float, count: int, step: float = 1.0) -> list[dict[str, Any]]:
    return [{"Period": index + 1, "Value": round(max(0.0, base + (index - count / 2) * step + ((index % 3) - 1) * step * 0.6), 2)} for index in range(count)]


def calculate_training_load(athletes: list[AthleteRow] | None = None) -> dict[str, Any]:
    athlete = _primary_athlete(athletes)
    if not athlete:
        return {"Acute Load": 0.0, "Chronic Load": 0.0, "Acute:Chronic Ratio": 0.0, "Data Label": DATA_LABEL}
    acute = athlete["Training Load"]
    chronic = athlete["Chronic Load"]
    return {"Acute Load": acute, "Chronic Load": chronic, "Acute:Chronic Ratio": round(acute / max(chronic, 1.0), 2), "Data Label": DATA_LABEL}


def calculate_workload(athletes: list[AthleteRow] | None = None) -> dict[str, list[dict[str, Any]]]:
    base = calculate_training_load(athletes)["Acute Load"]
    return {"Daily": _series(base, 14, 2.1), "Weekly": _series(base * 5.2, 8, 8.0), "Monthly": _series(base * 22.0, 6, 30.0)}


def calculate_fatigue_score(athletes: list[AthleteRow] | None = None) -> dict[str, Any]:
    athlete = _primary_athlete(athletes)
    score = _safe_float(athlete.get("Fatigue Score") if athlete else 0.0)
    band = "High" if score >= 70 else "Moderate" if score >= 38 else "Low"
    return {"Fatigue Score": round(score, 2), "Band": band, "Data Label": DATA_LABEL}


def calculate_recovery_score(athletes: list[AthleteRow] | None = None) -> dict[str, Any]:
    athlete = _primary_athlete(athletes)
    recovery = _safe_float(athlete.get("Recovery Score") if athlete else 0.0)
    sleep = _clamp(62.0 + recovery * 0.33)
    index = _clamp(recovery * 0.72 + sleep * 0.28)
    return {"Recovery %": round(recovery, 2), "Sleep Quality": round(sleep, 2), "Recovery Index": round(index, 2), "Data Label": DATA_LABEL}


def calculate_heart_rate_metrics(athletes: list[AthleteRow] | None = None) -> dict[str, Any]:
    athlete = _primary_athlete(athletes)
    avg_hr = _safe_float(athlete.get("Average HR") if athlete else 0.0)
    max_hr = _safe_float(athlete.get("Maximum HR") if athlete else 0.0)
    recovery_hr = _safe_float(athlete.get("Recovery HR") if athlete else 0.0)
    return {
        "Series": [
            {"Minute": minute, "Average HR": round(avg_hr + (minute % 9) * 0.6, 1), "Maximum HR": round(max_hr - max(0, 90 - minute) * 0.08, 1), "Recovery HR": round(recovery_hr + max(0, 15 - minute) * 0.4, 1)}
            for minute in range(0, 91, 5)
        ],
        "Average HR": round(avg_hr, 1),
        "Maximum HR": round(max_hr, 1),
        "Recovery HR": round(recovery_hr, 1),
        "Data Label": DATA_LABEL,
    }


def calculate_distance_covered(athletes: list[AthleteRow] | None = None) -> list[dict[str, Any]]:
    athlete = _primary_athlete(athletes)
    return [
        {"Zone": "Walking", "Distance": _safe_float(athlete.get("Walking") if athlete else 0.0)},
        {"Zone": "Jogging", "Distance": _safe_float(athlete.get("Jogging") if athlete else 0.0)},
        {"Zone": "Running", "Distance": _safe_float(athlete.get("Running") if athlete else 0.0)},
        {"Zone": "Sprint Distance", "Distance": _safe_float(athlete.get("Sprint Distance") if athlete else 0.0)},
    ]


def calculate_sprint_metrics(athletes: list[AthleteRow] | None = None) -> list[dict[str, Any]]:
    athlete = _primary_athlete(athletes)
    return [
        {"Metric": "Sprint Count", "Value": _safe_float(athlete.get("Sprint Count") if athlete else 0.0)},
        {"Metric": "Maximum Speed", "Value": _safe_float(athlete.get("Maximum Speed") if athlete else 0.0)},
        {"Metric": "Average Speed", "Value": _safe_float(athlete.get("Average Speed") if athlete else 0.0)},
    ]


def calculate_acceleration_metrics(athletes: list[AthleteRow] | None = None) -> list[dict[str, Any]]:
    athlete = _primary_athlete(athletes)
    sprint_count = _safe_float(athlete.get("Sprint Count") if athlete else 0.0)
    return [
        {"Zone": "0-1 m/s2", "Count": round(sprint_count * 1.8, 1)},
        {"Zone": "1-2 m/s2", "Count": round(sprint_count * 1.25, 1)},
        {"Zone": "2-3 m/s2", "Count": round(sprint_count * 0.72, 1)},
        {"Zone": "3+ m/s2", "Count": round(sprint_count * 0.36, 1)},
    ]


def calculate_deceleration_metrics(athletes: list[AthleteRow] | None = None) -> list[dict[str, Any]]:
    athlete = _primary_athlete(athletes)
    sprint_count = _safe_float(athlete.get("Sprint Count") if athlete else 0.0)
    return [
        {"Zone": "0 to -1 m/s2", "Count": round(sprint_count * 1.65, 1)},
        {"Zone": "-1 to -2 m/s2", "Count": round(sprint_count * 1.15, 1)},
        {"Zone": "-2 to -3 m/s2", "Count": round(sprint_count * 0.68, 1)},
        {"Zone": "-3+ m/s2", "Count": round(sprint_count * 0.3, 1)},
    ]


def calculate_high_intensity_runs(athletes: list[AthleteRow] | None = None) -> dict[str, list[dict[str, Any]]]:
    athlete = _primary_athlete(athletes)
    base = _safe_float(athlete.get("High Intensity Runs") if athlete else 0.0)
    return {"Runs per Match": _series(base, 8, 1.4), "Runs per Session": _series(base * 0.72, 10, 1.1)}


def calculate_wellness_score(athletes: list[AthleteRow] | None = None) -> dict[str, Any]:
    athlete = _primary_athlete(athletes)
    return {"Wellness Score": round(_safe_float(athlete.get("Wellness Score") if athlete else 0.0), 2), "Data Label": DATA_LABEL}


def calculate_readiness_score(athletes: list[AthleteRow] | None = None) -> dict[str, Any]:
    athlete = _primary_athlete(athletes)
    return {"Readiness Score": round(_safe_float(athlete.get("Readiness Score") if athlete else 0.0), 2), "Data Label": DATA_LABEL}


def calculate_performance_trends(athletes: list[AthleteRow] | None = None) -> dict[str, list[dict[str, Any]]]:
    athlete = _primary_athlete(athletes)
    base = _safe_float(athlete.get("SPORTA Score") if athlete else 0.0)
    return {"Matches": _series(base, 8, 1.8), "Training Sessions": _series(base * 0.92, 10, 1.4)}


def generate_athlete_summary(athletes: list[AthleteRow] | None = None) -> list[str]:
    rows = _athletes(athletes)
    if not rows:
        return ["No athlete monitoring data is available from the current player dataset."]
    load = calculate_training_load(rows)
    fatigue = calculate_fatigue_score(rows)
    recovery = calculate_recovery_score(rows)
    readiness = calculate_readiness_score(rows)
    sprints = calculate_high_intensity_runs(rows)["Runs per Session"]
    sprint_delta = sprints[-1]["Value"] - mean(item["Value"] for item in sprints[-4:-1]) if len(sprints) >= 4 else 0.0
    load_note = "within the optimal range" if 0.8 <= load["Acute:Chronic Ratio"] <= 1.3 else "outside the optimal range"
    sprint_note = "increased" if sprint_delta > 0 else "remained stable" if sprint_delta == 0 else "decreased"
    return [
        f"Training load remains {load_note} with an acute:chronic ratio of {load['Acute:Chronic Ratio']}.",
        f"Recovery score is {recovery['Recovery %']}% with a recovery index of {recovery['Recovery Index']}.",
        f"Sprint volume has {sprint_note} over the previous three sessions.",
        f"Fatigue indicators are {fatigue['Band'].lower()} at {fatigue['Fatigue Score']}/100.",
        f"Readiness is {readiness['Readiness Score']}/100 based on workload, wellness, recovery, and performance trend inputs.",
        DATA_LABEL,
    ]
