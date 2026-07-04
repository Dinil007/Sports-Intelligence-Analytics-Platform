"""MLOps Prediction Monitor Dashboard Component."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from mlops.monitoring.prediction_monitor import PredictionMonitor
from services.mlops_service import monitor_predictions


def render_prediction_monitor_dashboard() -> None:
    """Render prediction telemetry monitoring panel."""
    st.markdown("### 📡 Prediction Monitor")

    metrics = PredictionMonitor().get_metrics()

    if not metrics:
        st.info("No prediction metrics logged yet.")
    else:
        df = pd.DataFrame(metrics)
        latest = df.iloc[-1]

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Predictions",     f"{int(latest['prediction_count']):,}")
        c2.metric("Avg Latency",     f"{latest['latency_ms']:.1f} ms")
        c3.metric("Success Rate",    f"{latest['success_rate']:.2%}")
        c4.metric("Failures",        int(latest["failures"]))
        c5.metric("Avg Confidence",  f"{latest['avg_confidence']:.2%}")

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(
                df, x=df.index, y="latency_ms",
                title="Prediction Latency (ms)",
                color_discrete_sequence=["#38bdf8"],
                markers=True,
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", title_font_color="#f8fafc",
                xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(148,163,184,0.12)"),
            )
            st.plotly_chart(fig, use_container_width=True, key="latency_line")

        with col2:
            fig2 = px.area(
                df, x=df.index, y="prediction_count",
                title="Prediction Throughput",
                color_discrete_sequence=["#a78bfa"],
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", title_font_color="#f8fafc",
                xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(148,163,184,0.12)"),
            )
            st.plotly_chart(fig2, use_container_width=True, key="throughput_area")

    st.divider()

    with st.expander("📥 Log New Prediction Metrics"):
        with st.form("log_pred_form"):
            mc1, mc2 = st.columns(2)
            mid    = mc1.text_input("Model ID",          value="goals_predictor")
            cnt    = mc2.number_input("Prediction Count", value=1000, step=100)
            lat    = mc1.number_input("Avg Latency (ms)", value=35.0, step=1.0)
            sr     = mc2.slider("Success Rate",  0.0, 1.0, 0.99)
            fails  = mc1.number_input("Failures",         value=10, step=1)
            conf   = mc2.slider("Avg Confidence", 0.0, 1.0, 0.92)
            if st.form_submit_button("Log Metrics"):
                monitor_predictions(mid, int(cnt), float(lat), float(sr), int(fails), float(conf))
                st.success("Prediction metrics logged.")
                st.rerun()
