"""
dashboards/components/match_visualizations/xg_chart.py
=========================================================
Bar chart comparing xG between home and away teams.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.express as px
import streamlit as st


def render_xg_chart(team_stats: dict[str, Any]) -> None:
    """Render xG comparison as a bar chart.

    Parameters
    ----------
    team_stats : dict
        The ``team_statistics`` dict from ``get_match_dashboard()``.
        Reads ``team_stats["xg"]``.
    """
    xg = team_stats.get("xg", {})

    teams = list(xg.keys())
    values = [float(v) if v is not None else 0.0 for v in xg.values()]

    if not teams:
        st.info("No xG data available.")
        return

    colors = ["#3b82f6", "#ef4444"] if len(teams) >= 2 else ["#3b82f6"]

    fig = px.bar(
        x=teams,
        y=values,
        title="Expected Goals (xG)",
        labels={"x": "", "y": "xG"},
        text_auto=".2f",
        color=teams,
        color_discrete_sequence=colors,
    )
    fig.update_layout(
        height=300,
        yaxis=dict(range=[0, max(values) * 1.2] if values else [0, 1]),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True, key="match_xg_chart")
