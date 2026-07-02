"""Player radar chart."""

from __future__ import annotations

from typing import Any
import streamlit as st
import plotly.graph_objects as go

from services.player_intelligence_service import calculate_player_radar


def render_player_radar(events: list[dict[str, Any]]) -> None:
    """Render an interactive player radar chart."""
    st.subheader("Player Radar")
    if not events:
        st.info("No event data available for player radar.")
        return

    radar = calculate_player_radar(events)
    if not radar:
        st.info("No player radar data calculated.")
        return

    players = sorted(radar.keys())
    selected_player = st.selectbox("Select Player for Radar", players, key="player_intel_radar_select")
    values_map = radar.get(selected_player, {})
    metrics = [
        "passes",
        "shots",
        "carries",
        "pressures",
        "recoveries",
        "tackles",
        "progressive_passes",
        "progressive_carries",
    ]
    labels = [metric.replace("_", " ").title() for metric in metrics]
    raw_values = [float(values_map.get(metric, 0)) for metric in metrics]
    max_values = [max(float(row.get(metric, 0)) for row in radar.values()) or 1.0 for metric in metrics]
    normalized = [round(value / max_value * 10.0, 2) for value, max_value in zip(raw_values, max_values)]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=normalized + normalized[:1],
            theta=labels + labels[:1],
            fill="toself",
            name=selected_player,
            line=dict(color="#10b981", width=3),
            hovertemplate="%{theta}: %{r}/10<extra>" + selected_player + "</extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0, 0, 0, 0)",
            radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255, 255, 255, 0.15)", tickfont=dict(color="white")),
            angularaxis=dict(tickfont=dict(color="white")),
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        margin=dict(l=40, r=40, t=40, b=40),
        height=420,
    )

    st.plotly_chart(fig, use_container_width=True, key="player_intelligence_radar_plotly")
