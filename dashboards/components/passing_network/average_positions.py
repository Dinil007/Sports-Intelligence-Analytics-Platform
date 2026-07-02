"""
dashboards/components/passing_network/average_positions.py
============================================================
Renders average player positions on a football pitch.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from dashboards.components.pitch_visualizations.football_pitch import render_pitch
from services.passing_network_service import calculate_average_positions


def render_average_positions(events: list[dict[str, Any]]) -> None:
    """Render average player positions on a football pitch.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available for average positions.")
        return

    avg_positions = calculate_average_positions(events)
    if not avg_positions:
        st.info("No positions could be calculated.")
        return

    teams = list(avg_positions.keys())
    selected_team = st.selectbox("Select Team for Average Positions", teams, key="avg_pos_team_select")

    team_positions = avg_positions[selected_team]
    if not team_positions:
        st.warning(f"No positions found for {selected_team}.")
        return

    # Initialize pitch
    fig = render_pitch()

    # Draw player nodes vectorially
    x_coords = []
    y_coords = []
    names = []
    hover_texts = []
    counts = []

    for player, pos in team_positions.items():
        x_coords.append(pos["x"])
        y_coords.append(pos["y"])
        
        # Format label (Surname or last word)
        parts = player.split()
        short_name = parts[-1] if len(parts) > 1 else player
        names.append(short_name)
        counts.append(pos["count"])
        
        hover_texts.append(
            f"Player: {player}<br>"
            f"Passes: {pos['count']}<br>"
            f"Avg Coord: ({pos['x']:.1f}, {pos['y']:.1f})"
        )

    # Scale node sizes based on pass count
    max_count = max(counts) if counts else 1
    node_sizes = [12 + 18 * (c / max_count) for c in counts]

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="markers+text",
            marker=dict(
                size=node_sizes,
                color="#60a5fa",  # bright light blue
                line=dict(color="white", width=1.5),
            ),
            text=names,
            textposition="bottom center",
            textfont=dict(color="white", size=9),
            hoverinfo="text",
            hovertext=hover_texts,
            name="Player Average Position",
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Average Player Positions: {selected_team}",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(fig, use_container_width=True, key="avg_pos_chart_plotly")
