"""
dashboards/components/match_visualizations/ppda_chart.py
=========================================================
Bar chart comparing PPDA between home and away teams.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.express as px
import streamlit as st


def render_ppda_chart(team_stats: dict[str, Any]) -> None:
    """Render PPDA comparison as a bar chart.

    Parameters
    ----------
    team_stats : dict
        The ``team_statistics`` dict from ``get_match_dashboard()``.
        Reads ``team_stats["ppda"]``.
    """
    ppda = team_stats.get("ppda", {})

    teams = list(ppda.keys())
    values = [float(v) if v is not None else 0.0 for v in ppda.values()]

    if not teams:
        st.info("No PPDA data available.")
        return

    colors = ["#3b82f6", "#ef4444"] if len(teams) >= 2 else ["#3b82f6"]

    fig = px.bar(
        x=teams,
        y=values,
        title="PPDA (Passes Per Defensive Action)",
        labels={"x": "", "y": "PPDA"},
        text_auto=".1f",
        color=teams,
        color_discrete_sequence=colors,
    )
    fig.update_layout(
        height=300,
        yaxis=dict(range=[0, max(values) * 1.2] if values else [0, 10]),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True, key="match_ppda_chart")
