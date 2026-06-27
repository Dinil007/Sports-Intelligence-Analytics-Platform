"""Metric chip component for displaying KPIs in recommendation cards."""

from __future__ import annotations

import streamlit as st


def format_kpi(value, decimals: int = 1) -> str:
    """Format numeric KPI values for display."""
    if value is None:
        return "—"
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "—"


METRIC_LABELS = {
    "sporta_score": "SPORTA",
    "similarity": "Match",
    "goals": "Goals",
    "assists": "Assists",
    "total_xg": "xG",
    "passes": "Passes",
    "pass_accuracy": "Pass%",
    "dribbles": "Dribbles",
    "carries": "Carries",
    "recoveries": "Recoveries",
    "pressures": "Pressures",
    "progressive_passes": "Prog Passes",
    "minutes_played": "Minutes",
}


def get_metric_label(key: str) -> str:
    """Return human-readable label for a metric key."""
    return METRIC_LABELS.get(key, key.replace("_", " ").title())


def render_metrics(metrics: dict[str, object], num_columns: int = 6) -> None:
    """
    Render a row of metric cards using native Streamlit components.

    Parameters
    ----------
    metrics : dict[str, object]
        Key-value pairs of metric names to display values.
    num_columns : int
        Number of columns to distribute metrics across.
    """
    if not metrics:
        return

    cols = st.columns(num_columns)
    items = list(metrics.items())

    for i, (key, value) in enumerate(items):
        if i >= num_columns:
            break
        label = get_metric_label(key)
        display = format_kpi(value)
        with cols[i]:
            st.metric(label=label, value=display)
