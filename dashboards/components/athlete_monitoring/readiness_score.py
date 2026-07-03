from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.athlete_monitoring_service import calculate_readiness_score


def render_readiness_score() -> None:
    st.header("Readiness Score")
    data = calculate_readiness_score()
    fig = go.Figure(go.Indicator(mode="gauge+number", value=data["Readiness Score"], gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#84cc16"}}))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(data["Data Label"])
