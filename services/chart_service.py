"""
services/chart_service.py
=========================
Chart helper functions for the Player Comparison dashboard.

Keeps normalization and radar-data construction logic out of the UI layer so
it can be reused and unit-tested independently.
"""

from __future__ import annotations

import pandas as pd


# ---------------------------------------------------------------------------
# Radar chart configuration
# ---------------------------------------------------------------------------

# Elite benchmark caps — each metric is normalized to 0–100 against these.
# Tuned so that a world-class specialist reaches ~80–95 on their strength
# without any single metric dominating the radar shape.
RADAR_BENCHMARKS: dict[str, float] = {
    "sporta_score": 100.0,
    "goals":         50.0,
    "total_xg":      40.0,
    "shots":        500.0,
    "passes":     25000.0,
    "dribbles":    1000.0,
    "carries":    15000.0,
    "pressures":   3000.0,
    "recoveries":  1000.0,
}

# Short display labels paired with their column keys.
# Labels are kept brief to avoid overlap on the radar's angular axis.
RADAR_METRICS: list[tuple[str, str]] = [
    ("SPORTA",     "sporta_score"),
    ("Goals",      "goals"),
    ("xG",         "total_xg"),
    ("Shots",      "shots"),
    ("Passes",     "passes"),
    ("Dribbles",   "dribbles"),
    ("Carries",    "carries"),
    ("Recoveries", "recoveries"),
    ("Pressures",  "pressures"),
]

# Player colors — valid rgba() for fills (Plotly does NOT accept 8-digit hex),
# and plain hex for the outline strokes.
RADAR_PLAYER_COLORS: list[dict[str, str]] = [
    {"line": "rgb(59,130,246)", "fill": "rgba(59,130,246,0.20)"},   # blue
    {"line": "rgb(16,185,129)", "fill": "rgba(16,185,129,0.20)"},   # green
]


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def normalize_metric(value, max_value: float) -> float:
    """
    Normalize a single metric value to a 0–100 scale.

    Returns 0.0 for None / NaN / non-numeric inputs.
    Caps at 100.0 so an outlier never distorts the radar.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return 0.0
    try:
        f = float(value)
    except (TypeError, ValueError):
        return 0.0
    if max_value <= 0:
        return 0.0
    return min(f / max_value * 100.0, 100.0)


def get_available_metrics(columns) -> list[tuple[str, str]]:
    """
    Filter RADAR_METRICS to only those whose column key is present in
    *columns* (a pandas Index, list, or set).

    Both players share the same axes, so availability is determined once
    from the DataFrame columns.
    """
    col_set = set(columns)
    return [(lbl, col) for lbl, col in RADAR_METRICS if col in col_set]


def build_radar_data(player_row, metrics: list[tuple[str, str]]) -> tuple[list[str], list[float], list]:
    """
    Build normalized radar data for a single player.

    Parameters
    ----------
    player_row : pandas Series or dict-like
        A single row of scouting stats.
    metrics : list of (label, col_key)
        The metrics to include (already filtered to available columns).

    Returns
    -------
    (labels, values, raw_values) — all closed (first element appended) so the
    polygon renders correctly.  *values* are normalized 0–100; *raw_values*
    are the original numbers (for hover tooltips).
    """
    # Support both pandas Series and plain dict
    if hasattr(player_row, "index"):
        keys = set(player_row.index)
    elif isinstance(player_row, dict):
        keys = set(player_row.keys())
    else:
        keys = set()

    labels: list[str] = []
    values: list[float] = []
    raw_values: list = []

    for label, col in metrics:
        if col not in keys:
            continue
        raw = player_row.get(col)
        benchmark = RADAR_BENCHMARKS.get(col, 1.0)
        norm = normalize_metric(raw, benchmark)
        labels.append(label)
        values.append(norm)
        raw_values.append(raw)

    # Close the polygon
    if values:
        values.append(values[0])
        labels.append(labels[0])
        raw_values.append(raw_values[0])

    return labels, values, raw_values
