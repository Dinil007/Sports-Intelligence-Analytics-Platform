"""Possession chains renderer."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from services.team_intelligence_service import calculate_possession_chains


def render_possession_chains(events: list[dict[str, Any]]) -> None:
    """Render possession chain timeline, chart, and summary table."""
    st.markdown("### Possession Chains")
    data = calculate_possession_chains(events)
    summary = data.get("summary", {})
    chains = data.get("chains", [])
    if not summary:
        st.info("No possession chain data available.")
        return

    fig = go.Figure()
    for team in summary:
        team_chains = [chain for chain in chains if chain["team"] == team]
        fig.add_trace(
            go.Scatter(
                x=[chain["start_minute"] for chain in team_chains],
                y=[chain["events"] for chain in team_chains],
                mode="lines+markers",
                name=team,
            )
        )
    fig.update_layout(xaxis_title="Minute", yaxis_title="Chain length", height=360)
    st.plotly_chart(fig, use_container_width=True)

    teams = list(summary)
    fig_bar = go.Figure()
    fig_bar.add_bar(x=teams, y=[summary[team]["Average Chain Length"] for team in teams], name="Average Chain Length")
    fig_bar.add_bar(x=teams, y=[summary[team]["Longest Chain"] for team in teams], name="Longest Chain")
    fig_bar.update_layout(barmode="group", yaxis_title="Events", height=330)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.dataframe([{"Team": team, **values} for team, values in summary.items()], use_container_width=True)
