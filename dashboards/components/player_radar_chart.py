"""
dashboards/components/player_radar_chart.py
===========================================
Interactive Plotly radar chart comparing two players.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st


_METRICS = [
    "SPORTA Score",
    "Goals",
    "xG",
    "Passes",
    "Dribbles",
    "Carries",
    "Recoveries",
    "Pressures",
]

_METRIC_KEYS = {
    "SPORTA Score": "sporta_score",
    "Goals": "goals",
    "xG": "total_xg",
    "Passes": "passes",
    "Dribbles": "dribbles",
    "Carries": "carries",
    "Recoveries": "recoveries",
    "Pressures": "pressures",
}


def _get_metric(player: dict[str, Any], label: str) -> float:
    key = _METRIC_KEYS.get(label, "")
    if not key:
        return 0.0
    try:
        return float(player.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def _normalize(values: list[float]) -> list[float]:
    if not values:
        return [0.0] * len(_METRICS)
    peak = max(values)
    if peak <= 0:
        return [0.0] * len(values)
    return [min(100.0, (v / peak) * 100.0) for v in values]


def render_player_radar(
    selected_player: dict[str, Any],
    recommended_player: dict[str, Any],
    comparison_index: int = 0,
) -> None:
    """
    Render an interactive Plotly radar chart.

    Parameters
    ----------
    selected_player : dict[str, Any]
    recommended_player : dict[str, Any]
    """
    sel_raw = [_get_metric(selected_player, m) for m in _METRICS]
    rec_raw = [_get_metric(recommended_player, m) for m in _METRICS]
    sel_norm = _normalize(sel_raw)
    rec_norm = _normalize(rec_raw)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=rec_norm,
        theta=_METRICS,
        fill="toself",
        name="Recommended",
        line_color="blue",
    ))
    fig.add_trace(go.Scatterpolar(
        r=sel_norm,
        theta=_METRICS,
        fill="toself",
        name="Selected",
        line_color="red",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        width=None,
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        key=f"radar_{comparison_index}",
    )
