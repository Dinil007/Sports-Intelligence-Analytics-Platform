"""ml/recommendation_ranker.py
===============================
Weighted recommendation ranking engine.

Computes a 0-100 Recommendation Score from multiple weighted factors:
- Similarity (40%)
- SPORTA Score (30%)
- Age (10%)
- Recent Form (10%)
- Availability (10%)

This layer sits AFTER the similarity engine and BEFORE the UI layer.
"""

from __future__ import annotations

from typing import Any


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Return ``value`` as ``float``, falling back to ``default`` for invalid input."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _age_score(player: dict[str, Any]) -> float:
    """Age component mapped to a 0-100 scale.

    Preferred range is 20-27, with peak desirability at age 24.
    Missing age uses the neutral midpoint (50.0).
    """
    age = player.get("age")
    if age is None:
        return 50.0

    age = _safe_float(age)
    if 20.0 <= age <= 27.0:
        return 100.0

    if age < 20.0:
        # Linear ramp: 16 -> 0, 20 -> 100
        return max(0.0, (age - 16.0) / 4.0 * 100.0)

    # age > 27
    # Linear taper: 27 -> 100, 35 -> 0
    return max(0.0, (35.0 - age) / 8.0 * 100.0)


def _recent_form_score(player: dict[str, Any]) -> float:
    """Recent form component mapped to a 0-100 scale.

    Proxy: Goals + xG + Assists (no rolling form data available).
    Internal normalization caps raw contribution at 50.
    """
    goals = _safe_float(player.get("goals"), 0.0)
    xg = _safe_float(player.get("total_xg"), 0.0)
    assists = _safe_float(player.get("assists"), 0.0)
    raw = goals + xg + assists
    return min(raw, 50.0) / 50.0 * 100.0


def _availability_score(player: dict[str, Any]) -> float:
    """Availability component mapped to a 0-100 scale.

    Proxy: Minutes Played. Higher minutes indicate higher availability.
    Missing minutes uses the neutral midpoint (50.0).
    Internal normalization caps raw value at 3000 minutes.
    """
    minutes = player.get("minutes_played")
    if minutes is None:
        return 50.0

    minutes = _safe_float(minutes)
    return min(minutes, 3000.0) / 3000.0 * 100.0


def calculate_recommendation_score(player: dict[str, Any]) -> float:
    """Compute a 0-100 weighted Recommendation Score for a single player.

    Weights
    -------
    Similarity    40 %
    SPORTA Score 30 %
    Age          10 %
    Recent Form  10 %
    Availability 10 %

    Parameters
    ----------
    player : dict[str, Any]
        Player dictionary with display-ready fields. Missing numeric values
        are coerced to ``0.0`` (or neutral 50.0 where specified).

    Returns
    -------
    float
        Recommendation Score clamped to the range 0-100.
    """
    similarity = _safe_float(player.get("similarity_pct"), 0.0)
    sporta = _safe_float(player.get("sporta_score"), 0.0)
    age = _age_score(player)
    form = _recent_form_score(player)
    availability = _availability_score(player)

    score = (
        0.40 * similarity
        + 0.30 * sporta
        + 0.10 * age
        + 0.10 * form
        + 0.10 * availability
    )
    return max(0.0, min(100.0, score))


def rank_recommendations(players: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach ``recommendation_score`` to each player and sort descending.

    Parameters
    ----------
    players : list[dict[str, Any]]
        Already-ranked recommendation dicts as returned by the similarity
        engine / recommendation service.

    Returns
    -------
    list[dict[str, Any]]
        The same dicts with a new ``recommendation_score`` key added and
        reordered so the highest score appears first.
    """
    for player in players:
        player["recommendation_score"] = calculate_recommendation_score(player)

    players.sort(key=lambda p: p.get("recommendation_score", 0.0), reverse=True)
    return players
