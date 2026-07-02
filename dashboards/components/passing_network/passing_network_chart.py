"""
dashboards/components/passing_network/passing_network_chart.py
===============================================================
Renders the interactive passing network visualization.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from dashboards.components.pitch_visualizations.football_pitch import render_pitch
from services.passing_network_service import (
    calculate_average_positions,
    calculate_passing_connections,
)


def render_passing_network(events: list[dict[str, Any]]) -> None:
    """Render the interactive passing network on a football pitch.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available to generate the network.")
        return

    # Compute average positions and connections
    avg_positions = calculate_average_positions(events)
    connections = calculate_passing_connections(events)

    if not avg_positions:
        st.info("No positions could be calculated from passing data.")
        return

    teams = list(avg_positions.keys())
    selected_team = st.selectbox("Select Team for Passing Network", teams, key="pn_team_select")

    # Filter data for selected team
    team_positions = avg_positions[selected_team]
    team_connections = connections.get(selected_team, [])

    if not team_positions:
        st.warning(f"No player coordinates found for {selected_team}.")
        return

    # Count passes per player to scale node sizes
    pass_counts = {player: data["count"] for player, data in team_positions.items()}
    max_passes = max(pass_counts.values()) if pass_counts else 1

    # Filter connections (min threshold of 3 passes to avoid clutter)
    min_passes = st.slider(
        "Minimum Connection Strength (Passes)",
        min_value=1,
        max_value=20,
        value=3,
        key="pn_min_passes",
    )
    filtered_connections = [c for c in team_connections if c["count"] >= min_passes]

    # Initialize pitch figure
    fig = render_pitch()

    # Vectorized Edges using bins for varying widths
    # Groups: strong (>=10 passes), medium (5-9 passes), light (<5 passes)
    edge_bins = {
        "strong": {"x": [], "y": [], "width": 5.0, "color": "#10b981", "opacity": 0.85, "name": "Strong (10+ passes)"},
        "medium": {"x": [], "y": [], "width": 3.0, "color": "#3b82f6", "opacity": 0.70, "name": "Medium (5-9 passes)"},
        "light": {"x": [], "y": [], "width": 1.5, "color": "#9ca3af", "opacity": 0.45, "name": "Light (<5 passes)"},
    }

    for conn in filtered_connections:
        p1, p2 = conn["passer"], conn["receiver"]
        if p1 in team_positions and p2 in team_positions:
            x0, y0 = team_positions[p1]["x"], team_positions[p1]["y"]
            x1, y1 = team_positions[p2]["x"], team_positions[p2]["y"]
            cnt = conn["count"]

            if cnt >= 10:
                bin_key = "strong"
            elif cnt >= 5:
                bin_key = "medium"
            else:
                bin_key = "light"

            edge_bins[bin_key]["x"].extend([x0, x1, None])
            edge_bins[bin_key]["y"].extend([y0, y1, None])

    # Add edge traces to figure
    for _, edge_data in edge_bins.items():
        if edge_data["x"]:
            fig.add_trace(
                go.Scatter(
                    x=edge_data["x"],
                    y=edge_data["y"],
                    mode="lines",
                    line=dict(
                        color=edge_data["color"],
                        width=edge_data["width"],
                    ),
                    opacity=edge_data["opacity"],
                    name=edge_data["name"],
                    hoverinfo="none",
                )
            )

    # Vectorized Nodes
    node_x = []
    node_y = []
    node_sizes = []
    node_text = []
    node_hover = []

    for player, pos in team_positions.items():
        node_x.append(pos["x"])
        node_y.append(pos["y"])
        
        # Scale marker size (min: 15, max: 40)
        norm_passes = pass_counts[player] / max_passes
        node_sizes.append(15 + 25 * norm_passes)
        
        # Shorten player name for label (e.g. "Lionel Andrés Messi" -> "L. Messi" or Surname)
        parts = player.split()
        short_name = parts[-1] if len(parts) > 1 else player
        node_text.append(short_name)
        
        node_hover.append(
            f"Player: {player}<br>"
            f"Passes Made: {pass_counts[player]}<br>"
            f"Avg Position: ({pos['x']:.1f}, {pos['y']:.1f})"
        )

    # Add nodes trace
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            marker=dict(
                size=node_sizes,
                color="#eab308",  # vibrant gold
                line=dict(color="white", width=2),
            ),
            text=node_text,
            textposition="top center",
            textfont=dict(color="white", size=10),
            hoverinfo="text",
            hovertext=node_hover,
            name="Players",
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Passing Network: {selected_team}",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(fig, use_container_width=True, key="pn_chart_plotly")
