from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.scouting_service import get_player_profile

METRICS = ["goals", "assists", "xg", "xa", "passes", "carries", "pressures", "recoveries", "sporta_score"]


def render_player_comparison() -> None:
    st.header("Player Comparison")
    players = st.session_state.get("scouting_filtered_players") or st.session_state.get("scouting_players") or []
    names = [p["player_name"] for p in players]
    if len(names) < 2:
        st.info("Search at least two players to compare.")
        return
    c1, c2 = st.columns(2)
    p1 = c1.selectbox("Compare Player 1", names, key="scouting_compare_p1")
    p2 = c2.selectbox("Compare Player 2", names, index=1 if len(names) > 1 else 0, key="scouting_compare_p2")
    if p1 == p2:
        st.warning("Select two different players.")
        return
    rows = [get_player_profile(p1), get_player_profile(p2)]
    df = pd.DataFrame(rows)
    radar = go.Figure()
    for _, row in df.iterrows():
        values = [float(row.get(m, 0) or 0) for m in METRICS]
        max_v = max(values) or 1
        norm = [v / max_v * 100 for v in values]
        radar.add_trace(go.Scatterpolar(r=norm + norm[:1], theta=METRICS + METRICS[:1], fill="toself", name=row["player_name"]))
    radar.update_layout(height=420, polar=dict(radialaxis=dict(range=[0, 100])))
    st.plotly_chart(radar, use_container_width=True)
    long_df = df[["player_name"] + METRICS].melt(id_vars="player_name", var_name="metric", value_name="value")
    st.plotly_chart(px.bar(long_df, x="metric", y="value", color="player_name", barmode="group", title="Statistics Bar Chart"), use_container_width=True)
    st.dataframe(df[["player_name", "club", "position", "age"] + METRICS], use_container_width=True, hide_index=True)
