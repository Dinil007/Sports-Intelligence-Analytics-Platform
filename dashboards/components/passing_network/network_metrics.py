"""
dashboards/components/passing_network/network_metrics.py
==========================================================
Renders passing network graph-theory metrics.

Plotly only. No HTML. No CSS. No unsafe_allow_html.
"""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.passing_network_service import calculate_network_metrics


def render_network_metrics(events: list[dict[str, Any]]) -> None:
    """Render a table of network graph metrics for both teams.

    Parameters
    ----------
    events : list[dict]
        Passing events list.
    """
    if not events:
        st.info("No passing events available for network metrics.")
        return

    metrics = calculate_network_metrics(events)
    if not metrics:
        st.info("No network metrics calculated.")
        return

    teams = list(metrics.keys())
    if len(teams) == 0:
        st.warning("No team metrics available.")
        return

    # Use first and second team (if available)
    team1 = teams[0]
    team2 = teams[1] if len(teams) > 1 else None

    # Prepare row values
    headers = ["Passing Network Metric", team1]
    if team2:
        headers.append(team2)

    rows = [
        ["Most Connected Player", metrics[team1].get("most_connected_player", "N/A")],
        ["Passing Hub (Passes + Receipts)", metrics[team1].get("passing_hub", "N/A")],
        ["Network Density (0-1)", metrics[team1].get("network_density", 0.0)],
        ["Average Pass Length (Yards)", f"{metrics[team1].get('avg_pass_length', 0.0)} yds"],
    ]

    if team2:
        rows[0].append(metrics[team2].get("most_connected_player", "N/A"))
        rows[1].append(metrics[team2].get("passing_hub", "N/A"))
        rows[2].append(metrics[team2].get("network_density", 0.0))
        rows[3].append(f"{metrics[team2].get('avg_pass_length', 0.0)} yds")

    # Transpose rows for Plotly Table format
    col_metric = [r[0] for r in rows]
    col_team1 = [r[1] for r in rows]
    col_team2 = [r[2] for r in rows] if team2 else []

    cells_content = [col_metric, col_team1]
    if team2:
        cells_content.append(col_team2)

    # Render Plotly Table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=headers,
                    fill_color="#1e3a8a",
                    align="left",
                    font=dict(color="white", size=13, family="Outfit, Inter, sans-serif"),
                    height=30,
                ),
                cells=dict(
                    values=cells_content,
                    fill_color="#111827",
                    align="left",
                    font=dict(color="white", size=12, family="Outfit, Inter, sans-serif"),
                    height=30,
                    line_color="rgba(255, 255, 255, 0.1)",
                ),
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="Passing Network Graph Theory Metrics",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=20, r=20, t=50, b=20),
        height=220,
    )

    st.plotly_chart(fig, use_container_width=True, key="pn_metrics_table_plotly")
