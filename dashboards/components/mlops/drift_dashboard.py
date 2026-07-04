"""MLOps Drift Detection Dashboard Component."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.mlops_service import detect_data_drift, detect_model_drift, detect_concept_drift


def _demo_series(n: int = 30, mu: float = 0.5, sigma: float = 0.05) -> list[float]:
    rng = np.random.default_rng(42)
    return rng.normal(mu, sigma, n).clip(0, 1).tolist()


def render_drift_dashboard() -> None:
    """Render drift detection panels."""
    st.markdown("### 📡 Drift Detection")

    baseline = _demo_series(30, 0.50, 0.05)
    target   = _demo_series(30, 0.50, 0.05)   # no drift by default
    shifted  = _demo_series(30, 0.65, 0.08)   # shifted for model drift demo

    tab1, tab2, tab3 = st.tabs(["📊 Data Drift", "📉 Model Drift", "🔀 Concept Drift"])

    # ── Data Drift ─────────────────────────────────────────────────────────────
    with tab1:
        dd = detect_data_drift(baseline, target)
        col1, col2 = st.columns(2)
        col1.metric("PSI Score",  f"{dd['psi']:.4f}")
        col2.metric("Drift Detected", "Yes 🚨" if dd["has_drift"] else "No ✅")

        ts = list(range(len(baseline)))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ts, y=baseline, name="Baseline", line=dict(color="#38bdf8")))
        fig.add_trace(go.Scatter(x=ts, y=target,   name="Target",   line=dict(color="#f59e0b", dash="dash")))
        fig.update_layout(
            title="Feature Distribution: Baseline vs Target",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_color="#f8fafc",
            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(148,163,184,0.12)"),
        )
        st.plotly_chart(fig, use_container_width=True, key="data_drift_line")

    # ── Model Drift ────────────────────────────────────────────────────────────
    with tab2:
        baseline_acc = 0.87
        current_acc  = 0.81
        md = detect_model_drift(baseline_acc, current_acc)
        col1, col2 = st.columns(2)
        col1.metric("Accuracy Drop", f"{md['accuracy_drop']:.2%}")
        col2.metric("Drift Detected", "Yes 🚨" if md["has_drift"] else "No ✅")

        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_acc * 100,
            title={"text": "Current Model Accuracy (%)", "font": {"color": "#e2e8f0"}},
            gauge={
                "axis":    {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar":     {"color": "#22c55e" if not md["has_drift"] else "#ef4444"},
                "bgcolor": "rgba(0,0,0,0)",
                "steps":   [
                    {"range": [0, 70],  "color": "rgba(239,68,68,0.15)"},
                    {"range": [70, 85], "color": "rgba(245,158,11,0.15)"},
                    {"range": [85, 100],"color": "rgba(34,197,94,0.15)"},
                ],
                "threshold": {"line": {"color": "#f8fafc", "width": 2}, "thickness": 0.75, "value": baseline_acc * 100},
            },
            number={"font": {"color": "#f8fafc"}},
        ))
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", height=280)
        st.plotly_chart(fig2, use_container_width=True, key="model_drift_gauge")

    # ── Concept Drift ──────────────────────────────────────────────────────────
    with tab3:
        base_preds = _demo_series(25, 0.20, 0.04)
        curr_preds = _demo_series(25, 0.40, 0.07)
        cd = detect_concept_drift(base_preds, curr_preds)
        col1, col2 = st.columns(2)
        col1.metric("Mean Shift", f"{cd['mean_diff']:.4f}")
        col2.metric("Drift Detected", "Yes 🚨" if cd["has_drift"] else "No ✅")

        fig3 = px.scatter(
            x=list(range(len(base_preds))) + list(range(len(curr_preds))),
            y=base_preds + curr_preds,
            color=(["Baseline"] * len(base_preds)) + (["Current"] * len(curr_preds)),
            title="Concept Drift: Prediction Distribution Shift",
            color_discrete_map={"Baseline": "#38bdf8", "Current": "#f59e0b"},
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_color="#f8fafc",
        )
        st.plotly_chart(fig3, use_container_width=True, key="concept_drift_scatter")
