"""
dashboards/components/passing_network/team_shape.py
=====================================================
Renders team shape tactical dimensions.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.passing_network_service import calculate_team_shape


def render_team_shape(events: list[dict[str, Any]]) -> None:
    """Render a comparative grouped bar chart for team shape dimensions.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available for team shape.")
        return

    team_shapes = calculate_team_shape(events)
    if not team_shapes:
        st.info("No team shape data calculated.")
        return

    teams = list(team_shapes.keys())
    if not teams:
        st.info("No teams found for shape metrics.")
        return

    # Metrics to display
    metrics = ["width", "depth", "compactness", "attacking_line", "defensive_line"]
    labels = [
        "Team Width (Yards)",
        "Team Depth (Yards)",
        "Compactness (Avg Dist to Centroid)",
        "Attacking Line Height (Yards)",
        "Defensive Line Height (Yards)",
    ]

    fig = go.Figure()

    # Draw a bar for each team
    colors = ["#3b82f6", "#ef4444"]  # blue for first team, red for second team
    for idx, team in enumerate(teams):
        shape = team_shapes[team]
        values = [shape.get(m, 0.0) for m in metrics]

        fig.add_trace(
            go.Bar(
                name=team,
                x=labels,
                y=values,
                marker=dict(
                    color=colors[idx % len(colors)],
                    line=dict(color="white", width=1),
                ),
                text=values,
                textposition="auto",
                hovertemplate=f"Team: {team}<br>%{{x}}: %{{y}}<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(
            text="Team Shape & Tactical Line Height Comparisons",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            tickfont=dict(color="white"),
        ),
        yaxis=dict(
            title=dict(
                text="Yards / Distance Units",
                font=dict(color="white"),
            ),
            tickfont=dict(color="white"),
            gridcolor="rgba(255, 255, 255, 0.1)",
        ),
        barmode="group",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(
            font=dict(color="white"),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=50, r=20, t=60, b=50),
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True, key="team_shape_chart_plotly")
