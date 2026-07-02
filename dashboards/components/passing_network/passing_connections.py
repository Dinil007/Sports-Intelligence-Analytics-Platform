"""
dashboards/components/passing_network/passing_connections.py
==============================================================
Renders a chart of the top passing combinations.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.passing_network_service import calculate_passing_connections


def render_passing_connections(events: list[dict[str, Any]]) -> None:
    """Render a horizontal bar chart showing the strongest passing combinations.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available for passing connections.")
        return

    connections = calculate_passing_connections(events)
    if not connections:
        st.info("No passing combinations found.")
        return

    teams = list(connections.keys())
    selected_team = st.selectbox("Select Team for Passing Connections", teams, key="pn_conn_team_select")

    team_connections = connections.get(selected_team, [])
    if not team_connections:
        st.warning(f"No connections found for {selected_team}.")
        return

    # Slice the top 10 combinations
    top_connections = team_connections[:10]

    # Prepare labels and values
    combo_labels = []
    pass_counts = []
    
    for conn in reversed(top_connections):
        p1 = conn["passer"].split()[-1] if len(conn["passer"].split()) > 1 else conn["passer"]
        p2 = conn["receiver"].split()[-1] if len(conn["receiver"].split()) > 1 else conn["receiver"]
        combo_labels.append(f"{p1} → {p2}")
        pass_counts.append(conn["count"])

    # Render Horizontal Bar Chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=combo_labels,
            x=pass_counts,
            orientation="h",
            marker=dict(
                color=pass_counts,
                colorscale="Viridis",
                line=dict(color="white", width=1),
            ),
            text=pass_counts,
            textposition="auto",
            hovertemplate="Combination: %{y}<br>Passes: %{x}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Top 10 Passing Combinations: {selected_team}",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title=dict(
                text="Number of Passes",
                font=dict(color="white"),
            ),
            tickfont=dict(color="white"),
            gridcolor="rgba(255, 255, 255, 0.1)",
        ),
        yaxis=dict(
            tickfont=dict(color="white"),
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=150, r=20, t=50, b=50),
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True, key="pn_conn_chart_plotly")
