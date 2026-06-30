"""
dashboards/components/match_visualizations/progressive_pass_chart.py
=====================================================================
Grouped bar chart comparing progressive passes between teams.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st


def render_progressive_pass_chart(team_stats: dict[str, Any]) -> None:
    """Render progressive pass comparison as a grouped bar chart.

    Parameters
    ----------
    team_stats : dict
        The ``team_statistics`` dict from ``get_match_dashboard()``.
        Reads ``team_stats["progressive_passes"]``.
    """
    prog = team_stats.get("progressive_passes", {})
    repo = team_stats.get("repository", {})

    home = repo.get("home_team", "Home")
    away = repo.get("away_team", "Away")

    home_val = prog.get(home, 0) or 0
    away_val = prog.get(away, 0) or 0

    teams = [home, away]
    values = [home_val, away_val]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=teams,
        y=values,
        name="Progressive Passes",
        marker_color=["#3b82f6", "#ef4444"],
        text=[str(int(v)) for v in values],
        textposition="outside",
    ))

    fig.update_layout(
        title="Progressive Passes",
        yaxis=dict(title="Count", range=[0, max(values) * 1.3] if max(values) else [0, 10]),
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, key="match_progressive_pass_chart")
