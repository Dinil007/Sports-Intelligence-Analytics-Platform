"""MLOps Model Health Dashboard Component."""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.mlops_service import calculate_model_health, list_registered_models
from mlops.monitoring.prediction_monitor import PredictionMonitor
from mlops.monitoring.latency_monitor import LatencyMonitor


def render_model_health_dashboard() -> None:
    """Render model health index gauges for all production models."""
    st.markdown("### 💚 Model Health")

    models = list_registered_models()
    metrics = PredictionMonitor().get_metrics()

    if not models:
        st.info("No registered models to evaluate.")
        return

    prod_models = [m for m in models if m.get("stage") in {"Production", "Staging"}]
    if not prod_models:
        prod_models = models  # fall back to show all

    cols = st.columns(min(len(prod_models), 3))
    for i, model in enumerate(prod_models[:3]):
        mid = model["model_id"]
        # Find latest metrics for this model
        model_metrics = [mx for mx in metrics if mx.get("model_id") == mid]
        sr  = model_metrics[-1]["success_rate"]  if model_metrics else 0.995
        lat = model_metrics[-1]["latency_ms"]    if model_metrics else 35.0

        health = calculate_model_health(sr, lat, has_drift=False)
        lat_status = LatencyMonitor.get_latency_status(lat)

        color = "#22c55e" if health >= 80 else ("#f59e0b" if health >= 60 else "#ef4444")

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=health,
            title={"text": f"{model['name']}<br><sub>{model.get('stage','N/A')}</sub>", "font": {"color": "#e2e8f0", "size": 13}},
            delta={"reference": 90, "valueformat": ".1f"},
            gauge={
                "axis":    {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar":     {"color": color},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 60],  "color": "rgba(239,68,68,0.12)"},
                    {"range": [60, 80], "color": "rgba(245,158,11,0.12)"},
                    {"range": [80, 100],"color": "rgba(34,197,94,0.12)"},
                ],
            },
            number={"suffix": " / 100", "font": {"color": "#f8fafc"}},
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", height=250, margin=dict(t=60, b=10))
        with cols[i % 3]:
            st.plotly_chart(fig, use_container_width=True, key=f"health_gauge_{mid}")
            st.caption(f"Latency: {lat:.1f} ms — {lat_status} | Success: {sr:.2%}")
