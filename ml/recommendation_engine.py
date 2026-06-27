"""
ml/recommendation_engine.py
============================
Machine learning engine for player similarity recommendations.

Responsibilities:
- Prepare feature matrices from player data
- Normalize features for fair comparison
- Calculate cosine similarity between players
- Rank and return top-N recommendations

Algorithm: Cosine Similarity with L2 normalization.

No SQL.
No Streamlit.
Pure ML.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    import pandas as pd


# ---------------------------------------------------------------------------
# Feature configuration
# ---------------------------------------------------------------------------

FEATURE_COLUMNS = [
    "sporta_score",
    "goals",
    "total_xg",
    "passes",
    "dribbles",
    "carries",
    "recoveries",
    "pressures",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PlayerVector:
    """Immutable feature vector for a single player."""
    player_name: str
    team_name: str | None
    features: np.ndarray  # shape: (n_features,)

    @property
    def normalized(self) -> np.ndarray:
        """L2-normalized feature vector."""
        norm = np.linalg.norm(self.features)
        if norm == 0:
            return self.features
        return self.features / norm


@dataclass(frozen=True)
class SimilarityResult:
    """Result of similarity comparison between two players."""
    player_name: str
    team_name: str | None
    similarity: float  # 0-100 percentage
    sporta_score: float
    goals: float
    total_xg: float
    passes: float
    dribbles: float
    carries: float
    recoveries: float
    pressures: float


# ---------------------------------------------------------------------------
# Core ML functions
# ---------------------------------------------------------------------------

def prepare_feature_matrix(players: list[dict]) -> tuple[np.ndarray, list[str]]:
    """
    Build a feature matrix from a list of player dicts.
    
    Parameters
    ----------
    players : list[dict]
        Each dict must contain FEATURE_COLUMNS keys with numeric values.
    
    Returns
    -------
    X : np.ndarray
        Shape: (n_players, n_features). Missing values are set to 0.
    names : list[str]
        Player names in the same order as rows in X.
    """
    n_players = len(players)
    n_features = len(FEATURE_COLUMNS)
    
    X = np.zeros((n_players, n_features), dtype=np.float64)
    names: list[str] = []

    for i, player in enumerate(players):
        names.append(player.get("player_name", ""))
        for j, col in enumerate(FEATURE_COLUMNS):
            value = player.get(col)
            if value is None:
                X[i, j] = 0.0
            else:
                try:
                    X[i, j] = float(value)
                except (TypeError, ValueError):
                    X[i, j] = 0.0

    return X, names


def normalize_features(X: np.ndarray) -> np.ndarray:
    """
    L2-normalize each row (player vector) independently.
    
    Parameters
    ----------
    X : np.ndarray
        Shape: (n_players, n_features)
    
    Returns
    -------
    X_norm : np.ndarray
        L2-normalized matrix.
    """
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return X / norms


def calculate_similarity(
    target_vector: np.ndarray,
    candidate_vectors: np.ndarray,
) -> np.ndarray:
    """
    Compute cosine similarity between a target player and all candidates.
    
    Parameters
    ----------
    target_vector : np.ndarray
        Shape: (n_features,)
    candidate_vectors : np.ndarray
        Shape: (n_candidates, n_features)
    
    Returns
    -------
    similarities : np.ndarray
        Shape: (n_candidates,). Values are 0-1 cosine similarity scores.
    """
    # Normalize target
    norm_target = np.linalg.norm(target_vector)
    if norm_target == 0:
        return np.zeros(candidate_vectors.shape[0], dtype=np.float64)
    target_normed = target_vector / norm_target

    # Normalize candidates
    norms = np.linalg.norm(candidate_vectors, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    candidates_normed = candidate_vectors / norms

    # Cosine similarity = dot product of normalized vectors
    similarities = np.dot(candidates_normed, target_normed)
    return similarities


def rank_players(
    similarities: np.ndarray,
    players: list[dict],
    top_n: int = 10,
) -> list[SimilarityResult]:
    """
    Rank players by similarity and SPORTA Score, return top-N.
    
    Sort criteria:
    1. Highest similarity (descending)
    2. Highest SPORTA Score (descending) as tiebreaker
    
    Parameters
    ----------
    similarities : np.ndarray
        Cosine similarity scores for each player.
    players : list[dict]
        Player data dicts with additional fields for output.
    top_n : int
        Number of recommendations to return.
    
    Returns
    -------
    ranked : list[SimilarityResult]
        Top-N most similar players.
    """
    if len(similarities) == 0:
        return []

    # Build indexable list
    results = []
    for idx, player in enumerate(players):
        sim = float(similarities[idx])
        sporta_score = float(player.get("sporta_score") or 0)
        results.append({
            "idx": idx,
            "similarity": sim,
            "sporta_score": sporta_score,
        })

    # Sort: primary = similarity descending, secondary = sporta_score descending
    results.sort(key=lambda r: (r["similarity"], r["sporta_score"]), reverse=True)

    # Take top N
    top_results = results[:top_n]

    # Build output objects
    ranked = []
    for r in top_results:
        idx = r["idx"]
        player = players[idx]
        similarity_pct = round(r["similarity"] * 100, 1)

        ranked.append(SimilarityResult(
            player_name=player.get("player_name", ""),
            team_name=player.get("team_name"),
            similarity=similarity_pct,
            sporta_score=float(player.get("sporta_score") or 0),
            goals=float(player.get("goals") or 0),
            total_xg=float(player.get("total_xg") or 0),
            passes=float(player.get("passes") or 0),
            dribbles=float(player.get("dribbles") or 0),
            carries=float(player.get("carries") or 0),
            recoveries=float(player.get("recoveries") or 0),
            pressures=float(player.get("pressures") or 0),
        ))

    return ranked