"""
dashboards/components/visualizations/recommendation_goal_chart.py
==================================================================
Grouped bar chart showing Goals and Assists per recommended player.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st


def render_goal_contribution_chart(recommendations: list[dict[str, Any]]) -> None:
    """Grouped vertical bar chart of *goals* and *assists* per player.

    Parameters
    ----------
    recommendations : list[dict[str, Any]]
        Each dict must contain ``player_name``, ``goals``, and ``assists``.
    """
    if not recommendations:
        st.info("No goal contribution data available.")
        return

    # Sort descending by goals + assists
    sorted_recs = sorted(
        recommendations,
        key=lambda r: (
            float(r.get("goals", 0) or 0) + float(r.get("assists", 0) or 0)
        ),
        reverse=True,
    )

    names = [r.get("player_name", "Unknown") for r in sorted_recs]
    goals = [float(r.get("goals", 0) or 0) for r in sorted_recs]
    assists = [float(r.get("assists", 0) or 0) for r in sorted_recs]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names,
        y=goals,
        name="Goals",
        marker_color="indianred",
        text=[f"{v:.0f}" for v in goals],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        x=names,
        y=assists,
        name="Assists",
        marker_color="royalblue",
        text=[f"{v:.0f}" for v in assists],
        textposition="outside",
    ))

    fig.update_layout(
        title="Goal Contribution (Goals & Assists)",
        xaxis=dict(title=""),
        yaxis=dict(title="Count"),
        barmode="group",
        height=400,
        margin=dict(l=0, r=0, t=40, b=80),
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True, key="recommendation_goal_contribution_chart")
