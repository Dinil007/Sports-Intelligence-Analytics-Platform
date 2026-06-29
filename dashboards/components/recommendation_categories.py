"""Recommendation categories component – enterprise scouting categories (Phase 3.4.3).

Transforms an unordered recommendation list into scouting categories similar to
Wyscout, Hudl, and Stats Perform.

Design constraints
------------------
- Lightweight in-memory categorization only.
- No SQL.
- No AI / ML calls.
- No repository imports.
- No service imports.
- The recommendation engine output is never modified or re-ordered.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


BUDGET_TIER_ORDER = ["Low", "Medium", "High", "Elite"]


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Return *value* as float, falling back to *default* when None or invalid."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _best_overall(players: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Category: ⭐ Best Overall – highest SPORTA Score."""
    if not players:
        return None
    return max(players, key=lambda p: _safe_float(p.get("sporta_score")))


def _similar_playing_style(
    players: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Category: 🏃 Similar Playing Style – highest Similarity Score."""
    if not players:
        return None
    return max(players, key=lambda p: _safe_float(p.get("similarity_pct")))


def _young_prospect(players: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Category: 🌱 Young Prospect – youngest player (age must not be None).

    Returns None when every player has a None age, causing the section to be
    skipped entirely.
    """
    players_with_age = [p for p in players if p.get("age") is not None]
    if not players_with_age:
        return None
    return min(players_with_age, key=lambda p: _safe_float(p.get("age")))


def _budget_option(players: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Category: 💰 Budget Option – lowest Budget Tier.

    Fallback: when ``budget_tier`` is not present in the recommendation data
    (the dataset does not store budget tiers yet), the category instead
    selects the player with the lowest SPORTA Score among those whose
    Similarity Score is ≥ 70 %.
    """
    if not players:
        return None

    has_budget_tier = any("budget_tier" in p for p in players)
    if has_budget_tier:
        def _tier_key(p: dict) -> int:
            tier = p.get("budget_tier")
            if tier in BUDGET_TIER_ORDER:
                return BUDGET_TIER_ORDER.index(tier)
            return len(BUDGET_TIER_ORDER)  # Unknown / missing tier = most expensive

        return min(players, key=_tier_key)

    # Fallback: lowest SPORTA Score among players with Similarity ≥ 70 %
    eligible = [
        p for p in players if _safe_float(p.get("similarity_pct")) >= 70.0
    ]
    if not eligible:
        return None
    return min(eligible, key=lambda p: _safe_float(p.get("sporta_score")))


def _defensive_alternative(
    players: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Category: 🛡 Defensive Alternative – highest Recoveries + Pressures."""
    if not players:
        return None
    return max(
        players,
        key=lambda p: _safe_float(p.get("recoveries")) + _safe_float(p.get("pressures")),
    )


def _creative_alternative(
    players: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Category: 🎯 Creative Alternative – highest Passes + Progressive Passes + Assists."""
    if not players:
        return None
    return max(
        players,
        key=lambda p: (
            _safe_float(p.get("passes"))
            + _safe_float(p.get("progressive_passes"))
            + _safe_float(p.get("assists"))
        ),
    )


# Category definitions in strict priority order.
# Because players are removed from the pool after assignment, the highest-
# priority category always claims its top player first.
CATEGORY_SELECTORS = [
    ("⭐ Best Overall", _best_overall),
    ("🏃 Similar Playing Style", _similar_playing_style),
    ("🌱 Young Prospect", _young_prospect),
    ("💰 Budget Option", _budget_option),
    ("🛡 Defensive Alternative", _defensive_alternative),
    ("🎯 Creative Alternative", _creative_alternative),
]


def render_recommendation_categories(recommendations: list[dict[str, Any]]) -> None:
    """Render enterprise scouting categories for a list of recommendations.

    Categories are created entirely in-memory from already-returned
    recommendation data. No SQL, AI, or repository calls are made.

    Parameters
    ----------
    recommendations : list[dict[str, Any]]
        Ranked recommendation dicts as returned by the recommendation engine.
        Player fields are consumed but never mutated.
    """
    if not recommendations:
        return

    pool: list[dict[str, Any]] = list(recommendations)
    assigned: set[str] = set()

    for display_name, selector in CATEGORY_SELECTORS:
        if not pool:
            break

        player = selector(pool)
        if player is None:
            continue

        player_name = player.get("player_name")
        if player_name in assigned:
            continue

        assigned.add(player_name)
        pool.remove(player)

        st.subheader(display_name)
