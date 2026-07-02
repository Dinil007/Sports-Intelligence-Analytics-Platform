"""
dashboards/components/passing_network/progressive_network.py
=============================================================
Renders progressive passes mapped on the football pitch.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from dashboards.components.pitch_visualizations.football_pitch import render_pitch
from services.passing_network_service import calculate_progressive_passes


def render_progressive_network(events: list[dict[str, Any]]) -> None:
    """Render progressive passes on the football pitch.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available for progressive network.")
        return

    progressive_passes = calculate_progressive_passes(events)
    if not progressive_passes:
        st.info("No progressive passes identified.")
        return

    teams = list(progressive_passes.keys())
    selected_team = st.selectbox("Select Team for Progressive Passes", teams, key="prog_team_select")

    team_passes = progressive_passes.get(selected_team, [])
    if not team_passes:
        st.warning(f"No progressive passes found for {selected_team}.")
        return

    # Draw the pitch background
    fig = render_pitch()

    # Draw pass lines using a single vectorized trace with None separators
    line_x = []
    line_y = []
    for e in team_passes:
        sx, sy = e["location"]
        ex, ey = e["pass_end_location"]
        line_x.extend([sx, ex, None])
        line_y.extend([sy, ey, None])

    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            line=dict(
                color="#10b981",  # bright progressive green
                width=2.0,
            ),
            opacity=0.75,
            name="Progressive Pass path",
            showlegend=False,
            hoverinfo="none",
        )
    )

    # Draw pass destinations (heads of the paths)
    end_x = [e["pass_end_location"][0] for e in team_passes]
    end_y = [e["pass_end_location"][1] for e in team_passes]
    
    fig.add_trace(
        go.Scatter(
            x=end_x,
            y=end_y,
            mode="markers",
            marker=dict(
                size=6,
                color="#eab308",  # golden arrow tips
                symbol="triangle-up",
                line=dict(width=1, color="white"),
            ),
            name="Pass Target Destination",
        )
    )

    # Draw start positions (bases of the paths)
    start_x = [e["location"][0] for e in team_passes]
    start_y = [e["location"][1] for e in team_passes]

    fig.add_trace(
        go.Scatter(
            x=start_x,
            y=start_y,
            mode="markers",
            marker=dict(
                size=6,
                color="#3b82f6",  # blue start points
                line=dict(width=1, color="white"),
            ),
            hovertemplate=(
                "From: (%{x:.1f}, %{y:.1f})<br>"
                "Player: %{customdata[0]}<br>"
                "To: %{customdata[1]}<extra></extra>"
            ),
            customdata=[
                [
                    e.get("player_name"),
                    f"({e['pass_end_location'][0]:.1f}, {e['pass_end_location'][1]:.1f})",
                ]
                for e in team_passes
            ],
            name="Pass Origin Start",
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Progressive Passes: {selected_team} (Total: {len(team_passes)})",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(fig, use_container_width=True, key="prog_network_chart_plotly")
