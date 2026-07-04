"""ML Serving Monitor Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from services.monitoring_service import get_prediction_statistics, get_model_status, get_drift_status

def render_ml_monitor() -> None:
    """Render ML inference throughput, active model versions, and drift tracking."""
    st.markdown("### 🤖 ML Serving Monitoring")
    pred_data = get_prediction_statistics()
    models = get_model_status()
    drift = get_drift_status()
    
    stats = pred_data["stats"]
    st.markdown(f"**Serving Inference Engines:** `{stats['active_serving_models']} active` | **Total predictions (24h):** `{stats['total_predictions_24h']}` | **Inference latency:** `{stats['average_inference_time_ms']} ms (avg) / {stats['p95_inference_time_ms']} ms (p95)` ")
    
    c1, c2 = st.columns(2)
    
    # Prediction Throughput trends
    df_tp = pd.DataFrame(pred_data["throughput_trends"])
    fig_tp = px.line(
        df_tp, x="hour", y="predictions_count",
        title="Prediction Inference Requests",
        color_discrete_sequence=["#818cf8"],
    )
    fig_tp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c1.plotly_chart(fig_tp, use_container_width=True, key="ml_tp_line")
    
    # Model health gauge (Accuracy aggregate)
    avg_accuracy = sum(m["accuracy_metric"] for m in models) / len(models) if models else 0.0
    fig_acc = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_accuracy * 100,
        title={"text": "Average Model Serving Accuracy", "font": {"color": "#f8fafc", "size": 14}},
        number={"suffix": "%", "font": {"color": "#f8fafc", "size": 22}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#64748b"},
            "bar": {"color": "#6366f1"},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, 70], "color": "rgba(239,68,68,0.22)"},
                {"range": [70, 85], "color": "rgba(245,158,11,0.18)"},
                {"range": [85, 100], "color": "rgba(34,197,94,0.12)"},
            ]
        }
    ))
    fig_acc.update_layout(
        height=220, margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
    )
    c2.plotly_chart(fig_acc, use_container_width=True, key="ml_acc_gauge")
    
    # serving models & drift status
    st.markdown("#### Serving Deployed Models & Data Drift Analysis")
    tc1, tc2 = st.columns(2)
    tc1.write("**Model Version Status**")
    tc1.dataframe(pd.DataFrame(models), use_container_width=True, hide_index=True)
    
    # Drift details
    tc2.write("**Drift Scores**")
    drift_list = []
    for model_name, metrics in drift.items():
        if isinstance(metrics, dict):
            drift_list.append({
                "model": model_name,
                "psi (population stability index)": metrics["psi"],
                "ks_p_value": metrics["ks_p_value"],
                "drift_detected": metrics["drift_detected"],
            })
    tc2.dataframe(pd.DataFrame(drift_list), use_container_width=True, hide_index=True)
