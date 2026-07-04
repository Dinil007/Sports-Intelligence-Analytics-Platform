"""MLOps Executive Summary Dashboard Component."""
from __future__ import annotations

import streamlit as st

from services.mlops_service import (
    generate_mlops_summary, list_experiments, list_registered_models,
    get_training_history,
)
from mlops.monitoring.prediction_monitor import PredictionMonitor


def render_mlops_summary() -> None:
    """Render the executive MLOps summary panel."""
    st.markdown("### 📋 MLOps Executive Summary")

    summary = generate_mlops_summary()
    models  = list_registered_models()
    exps    = list_experiments()
    history = get_training_history()
    metrics = PredictionMonitor().get_metrics()

    # ── KPI strip ──────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Status",          summary.get("status", "Unknown"))
    k2.metric("Registered Models", len(models))
    k3.metric("Production Models", summary.get("production_models_count", 0))
    k4.metric("Tracked Experiments", len(exps))
    k5.metric("Training Runs",   len(history))

    st.divider()

    # ── Summary card ──────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            padding:1.4rem; border-radius:14px;
            background:linear-gradient(135deg,rgba(14,165,233,0.10),rgba(37,99,235,0.10));
            border:1px solid rgba(56,189,248,0.22); margin-bottom:1rem;
        ">
            <p style="color:#94a3b8;font-size:0.75rem;font-weight:700;text-transform:uppercase;margin:0 0 0.4rem;">
                Executive Summary
            </p>
            <p style="color:#f8fafc;font-size:1rem;line-height:1.6;margin:0;">
                {summary.get("summary", "")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Alerts ─────────────────────────────────────────────────────────────────
    alerts = summary.get("alerts_count", 0)
    if alerts == 0:
        st.success("✅ No active alerts. All systems operating within healthy thresholds.")
    else:
        st.warning(f"⚠️ {alerts} active alert(s) require attention.")

    # ── Per-model latency / health snapshot ───────────────────────────────────
    if metrics:
        st.markdown("**Latest Prediction Telemetry**")
        import pandas as pd
        df = pd.DataFrame(metrics)
        st.dataframe(
            df[["model_id", "prediction_count", "latency_ms", "success_rate", "avg_confidence", "timestamp"]].tail(5).style.format({
                "success_rate": "{:.2%}", "avg_confidence": "{:.2%}", "latency_ms": "{:.1f} ms"
            }),
            use_container_width=True, hide_index=True,
        )
