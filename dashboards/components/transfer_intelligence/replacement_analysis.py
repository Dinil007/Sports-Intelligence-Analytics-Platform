from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.transfer_intelligence_service import calculate_replacement_options


def render_replacement_analysis() -> None:
    st.header("Replacement Analysis")
    data = calculate_replacement_options()
    metrics = data.get("Metrics", [])
    if not metrics:
        st.info("No replacement comparison data is available.")
        return
    theta = metrics + metrics[:1]
    current = data.get("Current", []) + data.get("Current", [])[:1]
    replacement = data.get("Replacement", []) + data.get("Replacement", [])[:1]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=current, theta=theta, fill="toself", name=data.get("Current Player") or "Current Player"))
    fig.add_trace(go.Scatterpolar(r=replacement, theta=theta, fill="toself", name=data.get("Replacement Player") or "Replacement Player"))
    fig.update_layout(polar={"radialaxis": {"visible": True}}, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
