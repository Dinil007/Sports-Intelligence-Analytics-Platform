"""Tests for the recommendation engine ML pipeline."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.recommendation_engine import (
    FEATURE_COLUMNS,
    calculate_similarity,
    normalize_features,
    prepare_feature_matrix,
    rank_players,
)


def _make_player(name, sporta_score=80.0, goals=10, assists=5, total_xg=12.0,
                 passes=1000, dribbles=50, carries=200, recoveries=100, pressures=150, **kwargs):
    """Helper to create player dicts for tests."""
    data = {
        "player_name": name,
        "team_name": kwargs.get("team", "Test FC"),
        "sporta_score": sporta_score,
        "goals": goals,
        "assists": assists,
        "total_xg": total_xg,
        "passes": passes,
        "dribbles": dribbles,
        "carries": carries,
        "recoveries": recoveries,
        "pressures": pressures,
    }
    data.update(kwargs)
    return data


def test_prepare_feature_matrix_builds_correct_shape():
    players = [
        _make_player("Alice", sporta_score=90.0, goals=20),
        _make_player("Bob", sporta_score=85.0, goals=15),
    ]
    X, names = prepare_feature_matrix(players)
    assert X.shape == (2, len(FEATURE_COLUMNS))
    assert names == ["Alice", "Bob"]
    # Check that the sporta_score and goals columns are populated
    sporta_idx = FEATURE_COLUMNS.index("sporta_score")
    goals_idx = FEATURE_COLUMNS.index("goals")
    assert X[0, sporta_idx] == 90.0
    assert X[1, sporta_idx] == 85.0
    assert X[0, goals_idx] == 20.0
    assert X[1, goals_idx] == 15.0


def test_prepare_feature_matrix_handles_missing_values():
    """Missing numeric values should become 0.0."""
    players = [
        _make_player("Alice", goals=None),
        _make_player("Bob", sporta_score=None),
    ]
    X, names = prepare_feature_matrix(players)
    assert X.shape == (2, len(FEATURE_COLUMNS))
    goals_idx = FEATURE_COLUMNS.index("goals")
    sporta_idx = FEATURE_COLUMNS.index("sporta_score")
    assert X[0, goals_idx] == 0.0
    assert X[1, sporta_idx] == 0.0


def test_normalize_features_produces_unit_rows():
    X = np.array([
        [3.0, 4.0],
        [1.0, 0.0],
    ])
    X_norm = normalize_features(X)
    norms = np.linalg.norm(X_norm, axis=1)
    np.testing.assert_allclose(norms, np.ones(2), atol=1e-6)


def test_normalize_features_zero_row_does_not_crash():
    """Rows with all zeros should remain zero and not cause division by zero."""
    X = np.array([
        [0.0, 0.0],
        [1.0, 2.0],
    ])
    X_norm = normalize_features(X)
    assert X_norm[0, 0] == 0.0
    assert X_norm[0, 1] == 0.0
    norms = np.linalg.norm(X_norm, axis=1)
    np.testing.assert_allclose(norms, [0.0, 1.0], atol=1e-6)


def test_calculate_similarity_returns_expected_scores():
    target = np.array([1.0, 0.0])
    candidates = np.array([
        [1.0, 0.0],   # identical -> 1.0
        [0.0, 1.0],   # orthogonal -> 0.0
        [0.70710678, 0.70710678],  # 45 degrees -> ~0.707
    ])
    sims = calculate_similarity(target, candidates)
    assert sims.shape == (3,)
    assert abs(sims[0] - 1.0) < 1e-6
    assert abs(sims[1] - 0.0) < 1e-6
    assert abs(sims[2] - 0.7071) < 1e-3


def test_calculate_similarity_zero_target_returns_zeros():
    target = np.array([0.0, 0.0])
    candidates = np.array([[1.0, 1.0], [2.0, 2.0]])
    sims = calculate_similarity(target, candidates)
    np.testing.assert_allclose(sims, [0.0, 0.0])


def test_rank_players_sorts_correctly():
    players = [
        _make_player("A", sporta_score=70.0),
        _make_player("B", sporta_score=90.0),
        _make_player("C", sporta_score=80.0),
    ]
    similarities = np.array([0.8, 0.9, 0.85])
    ranked = rank_players(similarities, players, top_n=10)
    assert len(ranked) == 3
    # Primary sort: similarity descending
    assert ranked[0].player_name == "B"
    assert ranked[1].player_name == "C"
    assert ranked[2].player_name == "A"
    # Similarity should be converted to percentage
    assert ranked[0].similarity == 90.0


def test_rank_players_similarity_tiebreaker_uses_sporta_score():
    players = [
        _make_player("A", sporta_score=70.0),
        _make_player("B", sporta_score=90.0),
    ]
    similarities = np.array([0.9, 0.9])
    ranked = rank_players(similarities, players, top_n=10)
    # B has higher sporta_score and should rank first
    assert ranked[0].player_name == "B"
    assert ranked[1].player_name == "A"


def test_rank_players_respects_top_n():
    players = [_make_player(f"P{i}") for i in range(20)]
    similarities = np.linspace(0.1, 1.0, 20)
    ranked = rank_players(similarities, players, top_n=5)
    assert len(ranked) == 5
    assert ranked[0].player_name == "P19"
    assert ranked[-1].player_name == "P15"


def test_rank_players_empty_input_returns_empty():
    ranked = rank_players(np.array([]), [], top_n=10)
    assert ranked == []


def test_similarity_results_contain_expected_fields():
    players = [_make_player("Messi", sporta_score=95.0, goals=30)]
    similarities = np.array([1.0])
    ranked = rank_players(similarities, players, top_n=1)
    r = ranked[0]
    assert r.player_name == "Messi"
    assert r.similarity == 100.0
    assert r.sporta_score == 95.0
    assert r.goals == 30.0
    assert r.total_xg == 12.0
    assert r.passes == 1000.0
    assert r.dribbles == 50.0
    assert r.carries == 200.0
    assert r.recoveries == 100.0
    assert r.pressures == 150.0


if __name__ == "__main__":
    tests = [
        test_prepare_feature_matrix_builds_correct_shape,
        test_prepare_feature_matrix_handles_missing_values,
        test_normalize_features_produces_unit_rows,
        test_normalize_features_zero_row_does_not_crash,
        test_calculate_similarity_returns_expected_scores,
        test_calculate_similarity_zero_target_returns_zeros,
        test_rank_players_sorts_correctly,
        test_rank_players_similarity_tiebreaker_uses_sporta_score,
        test_rank_players_respects_top_n,
        test_rank_players_empty_input_returns_empty,
        test_similarity_results_contain_expected_fields,
    ]

    print("=== Running Recommendation Engine Tests ===")
    failed = 0
    for test in tests:
        print(f"[TEST] {test.__name__}...")
        try:
            test()
            print(f"[SUCCESS] {test.__name__}")
        except Exception as exc:
            failed += 1
            print(f"[FAILED] {test.__name__}: {exc}")

    if failed:
        print(f"\n[ERROR] {failed} test(s) failed.")
        raise SystemExit(1)
    print("\n[SUCCESS] All recommendation engine checks passed!")