"""
dashboards/components/visualizations/recommendation_similarity_chart.py
=======================================================================
Horizontal bar chart showing similarity percentage for each recommended
player.  Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.express as px
import streamlit as st


def render_similarity_chart(recommendations: list[dict[str, Any]]) -> None:
    """Horizontal bar chart of *similarity_pct* descending.

    Parameters
    ----------
    recommendations : list[dict[str, Any]]
        Each dict must contain ``player_name`` and ``similarity_pct``.
    """
    if not recommendations:
        st.info("No similarity data available.")
        return

    # Sort descending by similarity_pct
    sorted_recs = sorted(
        recommendations,
        key=lambda r: float(r.get("similarity_pct", 0) or 0),
        reverse=True,
    )

    names = [r.get("player_name", "Unknown") for r in sorted_recs]
    values = [float(r.get("similarity_pct", 0) or 0) for r in sorted_recs]

    fig = px.bar(
        x=values,
        y=names,
        orientation="h",
        title="Top Recommended Players — Similarity %",
        labels={"x": "Similarity %", "y": ""},
        text_auto=".1f",
        color=values,
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        height=400,
        xaxis=dict(range=[0, 105]),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True, key="recommendation_similarity_chart")
