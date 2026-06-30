"""
dashboards/components/visualizations/recommendation_sporta_chart.py
====================================================================
Vertical bar chart showing SPORTA Score for each recommended player.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.express as px
import streamlit as st


def render_sporta_score_chart(recommendations: list[dict[str, Any]]) -> None:
    """Vertical bar chart of *sporta_score* per player (descending).

    Parameters
    ----------
    recommendations : list[dict[str, Any]]
        Each dict must contain ``player_name`` and ``sporta_score``.
    """
    if not recommendations:
        st.info("No SPORTA Score data available.")
        return

    sorted_recs = sorted(
        recommendations,
        key=lambda r: float(r.get("sporta_score", 0) or 0),
        reverse=True,
    )

    names = [r.get("player_name", "Unknown") for r in sorted_recs]
    values = [float(r.get("sporta_score", 0) or 0) for r in sorted_recs]

    fig = px.bar(
        x=names,
        y=values,
        orientation="v",
        title="Player SPORTA Score",
        labels={"x": "", "y": "SPORTA Score"},
        text_auto=".1f",
        color=values,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        height=400,
        yaxis=dict(range=[0, 105]),
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=40, b=80),
        xaxis_tickangle=-45,
    )
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True, key="recommendation_sporta_score_chart")
