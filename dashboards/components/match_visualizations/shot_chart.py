"""
dashboards/components/match_visualizations/shot_chart.py
==========================================================
Vertical grouped bar chart comparing shots between home and away teams.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st


def render_shot_chart(team_stats: dict[str, Any]) -> None:
    """Render shot comparison as a grouped vertical bar chart.

    Parameters
    ----------
    team_stats : dict
        The ``team_statistics`` dict from ``get_match_dashboard()``.
        Reads ``team_stats["metrics"]`` for shot counts.
    """
    metrics = team_stats.get("metrics", {})
    repo = team_stats.get("repository", {})

    home = repo.get("home_team")
    away = repo.get("away_team")

    home_shots = 0
    away_shots = 0

    if home and home in metrics:
        home_shots = metrics[home].get("shots", 0) or 0
    elif repo.get("home_shots"):
        home_shots = repo["home_shots"]

    if away and away in metrics:
        away_shots = metrics[away].get("shots", 0) or 0
    elif repo.get("away_shots"):
        away_shots = repo["away_shots"]

    teams = [home or "Home", away or "Away"]
    shots = [home_shots, away_shots]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=teams,
        y=shots,
        name="Shots",
        marker_color=["#3b82f6", "#ef4444"],
        text=[str(int(s)) for s in shots],
        textposition="outside",
    ))

    fig.update_layout(
        title="Shot Comparison",
        yaxis=dict(title="Shots", range=[0, max(shots) * 1.3] if shots else [0, 10]),
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True, key="match_shot_chart")
