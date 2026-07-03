from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from services.scouting_service import calculate_player_performance


def render_performance_dashboard() -> None:
    st.header("Performance Dashboard")
    player_name = st.session_state.get("scouting_selected_player")
    if not player_name:
        st.info("Select a player to render performance dashboard.")
        return
    data = calculate_player_performance(player_name)
    if not data:
        st.warning("Performance data unavailable.")
        return
    radar = data.get("radar", {})
    labels = list(radar.keys())
    values = list(radar.values())
    fig_radar = go.Figure(go.Scatterpolar(r=values + values[:1], theta=labels + labels[:1], fill="toself", name=player_name))
    fig_radar.update_layout(height=420, polar=dict(radialaxis=dict(range=[0, 100])), showlegend=False)
    st.plotly_chart(fig_radar, use_container_width=True)

    trend_df = pd.DataFrame(data.get("trend", []))
    if not trend_df.empty:
        st.plotly_chart(px.line(trend_df, x="period", y="score", markers=True, title="Performance Trend"), use_container_width=True)

    c1, c2, c3 = st.columns(3)
    for col, title, values_dict in [
        (c1, "Passing Profile", data.get("passing_profile", {})),
        (c2, "Defensive Profile", data.get("defensive_profile", {})),
        (c3, "Attacking Profile", data.get("attacking_profile", {})),
    ]:
        with col:
            df = pd.DataFrame({"metric": list(values_dict.keys()), "value": list(values_dict.values())})
            st.plotly_chart(px.bar(df, x="metric", y="value", title=title), use_container_width=True)
