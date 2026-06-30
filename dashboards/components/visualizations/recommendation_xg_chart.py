"""
dashboards/components/visualizations/recommendation_xg_chart.py
================================================================
Horizontal bar chart comparing total xG per recommended player.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.express as px
import streamlit as st


def render_xg_chart(recommendations: list[dict[str, Any]]) -> None:
    """Horizontal bar chart of *total_xg* per player (descending).

    Parameters
    ----------
    recommendations : list[dict[str, Any]]
        Each dict must contain ``player_name`` and ``total_xg``.
    """
    if not recommendations:
        st.info("No xG data available.")
        return

    sorted_recs = sorted(
        recommendations,
        key=lambda r: float(r.get("total_xg", 0) or 0),
        reverse=True,
    )

    names = [r.get("player_name", "Unknown") for r in sorted_recs]
    values = [float(r.get("total_xg", 0) or 0) for r in sorted_recs]

    fig = px.bar(
        x=values,
        y=names,
        orientation="h",
        title="Player Total xG",
        labels={"x": "Total xG", "y": ""},
        text_auto=".2f",
        color=values,
        color_continuous_scale="Reds",
    )
    fig.update_layout(
        height=400,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True, key="recommendation_xg_chart")
