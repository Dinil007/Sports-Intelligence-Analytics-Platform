"""
dashboards/components/passing_network/passing_zones.py
========================================================
Renders passing zone distributions across pitch thirds.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.passing_network_service import calculate_zone_distribution


def render_passing_zones(events: list[dict[str, Any]]) -> None:
    """Render a stacked horizontal bar chart of zone distributions.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available for passing zones.")
        return

    distributions = calculate_zone_distribution(events)
    if not distributions:
        st.info("No zone distributions calculated.")
        return

    teams = list(distributions.keys())
    if not teams:
        st.info("No teams found for zone metrics.")
        return

    # Prepare data arrays for vectorized plotting
    defensive_vals = []
    middle_vals = []
    final_vals = []

    for team in teams:
        dist = distributions[team]
        defensive_vals.append(dist.get("defensive_third", 0.0))
        middle_vals.append(dist.get("middle_third", 0.0))
        final_vals.append(dist.get("final_third", 0.0))

    fig = go.Figure()

    # Add Defensive Third segment
    fig.add_trace(
        go.Bar(
            y=teams,
            x=defensive_vals,
            name="Defensive Third (< 40m)",
            orientation="h",
            marker=dict(color="#1e3a8a", line=dict(color="white", width=1)),
            text=[f"{v}%" for v in defensive_vals],
            textposition="auto",
            hovertemplate="Team: %{y}<br>Defensive Third: %{x}%<extra></extra>",
        )
    )

    # Add Middle Third segment
    fig.add_trace(
        go.Bar(
            y=teams,
            x=middle_vals,
            name="Middle Third (40m - 80m)",
            orientation="h",
            marker=dict(color="#3b82f6", line=dict(color="white", width=1)),
            text=[f"{v}%" for v in middle_vals],
            textposition="auto",
            hovertemplate="Team: %{y}<br>Middle Third: %{x}%<extra></extra>",
        )
    )

    # Add Final Third segment
    fig.add_trace(
        go.Bar(
            y=teams,
            x=final_vals,
            name="Final Third (> 80m)",
            orientation="h",
            marker=dict(color="#10b981", line=dict(color="white", width=1)),
            text=[f"{v}%" for v in final_vals],
            textposition="auto",
            hovertemplate="Team: %{y}<br>Final Third: %{x}%<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text="Pass Origin Zone Distribution (Pitch Thirds)",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title=dict(
                text="Percentage of Passes (%)",
                font=dict(color="white"),
            ),
            tickfont=dict(color="white"),
            range=[0, 100],
            gridcolor="rgba(255, 255, 255, 0.1)",
        ),
        yaxis=dict(
            tickfont=dict(color="white"),
        ),
        barmode="stack",
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
        margin=dict(l=150, r=20, t=60, b=50),
        height=300,
    )

    st.plotly_chart(fig, use_container_width=True, key="passing_zones_chart_plotly")
