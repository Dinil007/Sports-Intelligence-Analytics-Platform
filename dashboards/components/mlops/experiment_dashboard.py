"""MLOps Experiment Tracking Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.mlops_service import list_experiments, track_experiment


def render_experiment_dashboard() -> None:
    """Render experiment tracking section."""
    st.markdown("### 🧪 Experiment Tracking")

    experiments = list_experiments()

    if not experiments:
        st.info("No experiments tracked yet.")
        return

    df = pd.DataFrame(experiments)

    # ── KPI strip ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Experiments", len(df))
    c2.metric("Best Accuracy", f"{df['accuracy'].max():.2%}")
    c3.metric("Avg F1 Score",   f"{df['f1'].mean():.2%}")
    c4.metric("Algorithms", df["algorithm"].nunique())

    st.divider()

    # ── Accuracy line chart ────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(
            df, x="experiment_id", y="accuracy",
            title="Experiment Accuracy Over Runs",
            markers=True,
            color_discrete_sequence=["#38bdf8"],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_color="#f8fafc",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
        )
        st.plotly_chart(fig, use_container_width=True, key="exp_accuracy_line")

    with col2:
        fig2 = px.bar(
            df, x="experiment_id", y="training_time",
            title="Training Duration (seconds)",
            color="algorithm",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_color="#f8fafc",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
        )
        st.plotly_chart(fig2, use_container_width=True, key="exp_training_bar")

    # ── Data table ─────────────────────────────────────────────────────────────
    st.markdown("**All Experiments**")
    display_cols = ["experiment_id", "model_name", "algorithm", "accuracy", "precision", "recall", "f1", "model_version"]
    st.dataframe(df[display_cols].style.format({
        "accuracy": "{:.2%}", "precision": "{:.2%}", "recall": "{:.2%}", "f1": "{:.2%}"
    }), use_container_width=True, hide_index=True)

    # ── Track new experiment form ──────────────────────────────────────────────
    with st.expander("➕ Track New Experiment"):
        with st.form("new_experiment_form"):
            ec1, ec2 = st.columns(2)
            exp_id     = ec1.text_input("Experiment ID", value="exp_auto")
            model_name = ec2.text_input("Model Name",    value="goals_predictor")
            algo       = ec1.text_input("Algorithm",     value="XGBoost")
            dataset    = ec2.text_input("Dataset",       value="matches_2025")
            acc  = ec1.slider("Accuracy",  0.0, 1.0, 0.85)
            prec = ec2.slider("Precision", 0.0, 1.0, 0.83)
            rec  = ec1.slider("Recall",    0.0, 1.0, 0.82)
            f1   = ec2.slider("F1 Score",  0.0, 1.0, 0.82)
            fc   = ec1.number_input("Feature Count",  value=10, step=1)
            tt   = ec2.number_input("Training Time (s)", value=120.0)
            mv   = st.text_input("Model Version", value="1.0.0")

            if st.form_submit_button("Track Experiment"):
                track_experiment(exp_id, model_name, algo, acc, prec, rec, f1, float(tt), dataset, int(fc), mv)
                st.success(f"Experiment `{exp_id}` tracked.")
                st.rerun()
