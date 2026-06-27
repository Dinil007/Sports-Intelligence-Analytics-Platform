"""
services/recommendation_service.py
====================================
Business logic layer for player similarity recommendations.

Orchestrates data access and ML similarity calculations.
Returns structured recommendation results for the UI layer.

Never returns pandas DataFrames.
"""

from __future__ import annotations

import time
import numpy as np
from typing import Any

from database.db_connection import engine
from database.recommendation_repository import get_candidate_players, get_player, get_player_vector
from ml.recommendation_engine import (
    FEATURE_COLUMNS,
    calculate_similarity,
    prepare_feature_matrix,
    rank_players,
)


def recommend_similar_players(
    player_name: str,
    position: str | None = None,
    age_min: int | None = None,
    age_max: int | None = None,
    nationality: str | None = None,
    club: str | None = None,
    competition: str | None = None,
    season: str | None = None,
    budget_tier: str | None = None,
    preferred_foot: str | None = None,
    minutes_played_min: int | None = None,
    minutes_played_max: int | None = None,
    top_n: int = 10,
) -> list[dict[str, Any]]:
    """
    Recommend players similar to the selected player using ML cosine similarity.

    Parameters
    ----------
    player_name : str
        The reference player to find similarities for.
    position : str, optional
        Filter candidates by position (not yet enforced due to dataset limits).
    age_min : int, optional
        Minimum age filter (not yet enforced due to dataset limits).
    age_max : int, optional
        Maximum age filter (not yet enforced due to dataset limits).
    competition : str, optional
        Filter candidates by competition.
    season : str, optional
        Filter candidates by season.
    top_n : int
        Maximum number of recommendations to return (default: 10).

    Returns
    -------
    list[dict[str, Any]]
        Ranked recommendations, each containing:
        - player_name
        - team
        - competition
        - sporta_score
        - similarity (percentage)
        - goals, assists, total_xg, passes, dribbles, carries, recoveries, pressures

        Returns empty list if:
        - Reference player not found
        - No valid candidates
        - ML calculation fails
    """
    t0 = time.perf_counter()
    print("STEP 1 - Enter service")

    with engine.connect() as conn:
        print("STEP 2 - Fetch selected player")
        _t = time.perf_counter()
        selected = get_player(player_name, conn=conn)
        print(f"Query took {time.perf_counter()-_t:.2f}s")
        _t = time.perf_counter()
        target_vector = get_player_vector(player_name, conn=conn, player=selected)
        print(f"Query took {time.perf_counter()-_t:.2f}s")
        if target_vector is None:
            print("Returning empty (no vector)")
            print(f"Total time: {time.perf_counter()-t0:.2f}s")
            return []

        print("STEP 3 - Build player vector")
        target_features = np.array([target_vector[col] for col in FEATURE_COLUMNS], dtype=float)

        print("STEP 4 - Fetch candidate players")
        _t = time.perf_counter()
        candidates = get_candidate_players(
            position=position,
            age_min=age_min,
            age_max=age_max,
            nationality=nationality,
            club=club,
            competition=competition,
            season=season,
            budget_tier=budget_tier,
            preferred_foot=preferred_foot,
            minutes_played_min=minutes_played_min,
            minutes_played_max=minutes_played_max,
            conn=conn,
        )
        print(f"Query took {time.perf_counter()-_t:.2f}s")
        print("STEP 5 - Candidate count:", len(candidates))

    # 3. Exclude selected player
    candidates = [c for c in candidates if c.get("player_name") != player_name]

    # 4. Remove duplicates (keep first occurrence)
    seen = set()
    unique_candidates = []
    for c in candidates:
        name = c.get("player_name")
        if name and name not in seen:
            seen.add(name)
            unique_candidates.append(c)
    candidates = unique_candidates

    # 5. Ignore incomplete records (missing any required feature)
    complete_candidates = []
    for c in candidates:
        if all(c.get(col) is not None for col in FEATURE_COLUMNS):
            complete_candidates.append(c)
    candidates = complete_candidates

    if not candidates:
        return []

    print("STEP 6 - Feature matrix")
    _t = time.perf_counter()
    X, names = prepare_feature_matrix(candidates)
    print(f"Query took {time.perf_counter()-_t:.2f}s")
    if X.shape[0] == 0:
        return []

    print("STEP 7 - Cosine similarity")
    _t = time.perf_counter()
    similarities = calculate_similarity(target_features, X)
    print(f"Query took {time.perf_counter()-_t:.2f}s")

    print("STEP 8 - Ranking")
    _t = time.perf_counter()
    ranked = rank_players(similarities, candidates, top_n=top_n)
    print(f"Query took {time.perf_counter()-_t:.2f}s")

    print("STEP 9 - Returning")
    print(f"Total time: {time.perf_counter()-t0:.2f}s")

    results = []
    for r in ranked:
        tier = _sporta_tier(r.sporta_score)
        results.append({
            "player_name": r.player_name,
            "club": r.team_name or "N/A",
            "nationality": "N/A",
            "position": "N/A",
            "age": None,
            "minutes_played": None,
            "sporta_score": r.sporta_score,
            "sporta_tier": tier,
            "similarity_pct": r.similarity,
            "badge_color": _badge_color(tier),
            "goals": r.goals,
            "assists": 0,
            "total_xg": r.total_xg,
            "pass_accuracy": None,
            "passes": r.passes,
            "dribbles": r.dribbles,
            "carries": r.carries,
            "recoveries": r.recoveries,
            "pressures": r.pressures,
            "progressive_passes": None,
            "preferred_foot": "N/A",
        })

    return results


# Import numpy locally to avoid hard dependency at module level for non-ML paths
import numpy as np  # noqa: E402


def _sporta_tier(score: float) -> str:
    """Map SPORTA score to a tier label."""
    if score >= 85:
        return "Elite"
    if score >= 70:
        return "High"
    if score >= 55:
        return "Medium"
    return "Low"


def _badge_color(tier: str) -> str:
    """Map tier to a color class for UI rendering."""
    mapping = {
        "Elite": "#ef4444",
        "High": "#f59e0b",
        "Medium": "#3b82f6",
        "Low": "#10b981",
    }
    return mapping.get(tier, "#64748b")
