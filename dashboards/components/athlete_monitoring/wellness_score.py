from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.athlete_monitoring_service import calculate_wellness_score


def render_wellness_score() -> None:
    st.header("Wellness Score")
    data = calculate_wellness_score()
    fig = go.Figure(go.Indicator(mode="gauge+number", value=data["Wellness Score"], gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#14b8a6"}}))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(data["Data Label"])
