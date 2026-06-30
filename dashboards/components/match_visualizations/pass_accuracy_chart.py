"""
dashboards/components/match_visualizations/pass_accuracy_chart.py
==================================================================
Horizontal bar chart for pass accuracy comparison.
Plotly only — no HTML, no CSS, no unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any

import plotly.express as px
import streamlit as st


def render_pass_accuracy_chart(team_stats: dict[str, Any]) -> None:
    """Render pass accuracy comparison as a horizontal bar chart.

    Parameters
    ----------
    team_stats : dict
        The ``team_statistics`` dict from ``get_match_dashboard()``.
        Reads ``team_stats["pass_accuracy"]``.
    """
    pass_accuracy = team_stats.get("pass_accuracy", {})

    teams = list(pass_accuracy.keys())
    values = [float(v) if v is not None else 0.0 for v in pass_accuracy.values()]

    if not teams:
        st.info("No pass accuracy data available.")
        return

    colors = ["#3b82f6", "#ef4444"] if len(teams) >= 2 else ["#3b82f6"]

    fig = px.bar(
        x=values,
        y=teams,
        orientation="h",
        title="Pass Accuracy",
        labels={"x": "Pass Accuracy %", "y": ""},
        text_auto=".1f",
        color=teams,
        color_discrete_sequence=colors,
    )
    fig.update_layout(
        height=300,
        xaxis=dict(range=[0, 105]),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True, key="match_pass_accuracy_chart")
