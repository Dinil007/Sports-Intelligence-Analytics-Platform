"""MLOps Retraining Pipeline Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.mlops_service import run_retraining, schedule_retraining, get_training_history


def render_retraining_dashboard() -> None:
    """Render the retraining pipeline trigger panel."""
    st.markdown("### 🔄 Retraining Pipeline")

    col1, col2 = st.columns(2)
    with col1:
        with st.form("retraining_trigger_form"):
            st.markdown("**Trigger Manual Retraining**")
            model_name = st.text_input("Model Name", value="goals_predictor", key="retrain_model")
            dataset    = st.text_input("Dataset",    value="matches_2025_v1", key="retrain_ds")
            if st.form_submit_button("🚀 Run Retraining"):
                result = run_retraining(model_name, dataset)
                st.success(f"Retraining complete. New accuracy: `{result.get('new_accuracy', 0):.2%}`")
                st.rerun()

    with col2:
        with st.form("retraining_schedule_form"):
            st.markdown("**Schedule Automated Retraining**")
            sched_model = st.text_input("Model Name",        value="goals_predictor", key="sched_model")
            interval    = st.number_input("Interval (days)", value=7, step=1)
            if st.form_submit_button("📅 Schedule"):
                result = schedule_retraining(sched_model, int(interval))
                st.success(f"Scheduled every {interval} day(s). Status: `{result.get('status')}`")

    st.divider()
    render_training_history()


def render_training_history() -> None:
    """Render training run history chart and table."""
    st.markdown("### 📜 Training History")

    history = get_training_history()
    if not history:
        st.info("No training runs recorded yet.")
        return

    df = pd.DataFrame(history)

    fig = px.timeline(
        df.assign(start=df["timestamp"], end=df["timestamp"]),
        x_start="start", x_end="end",
        y="model_name",
        color="status",
        title="Training Run Timeline",
        color_discrete_map={"Success": "#22c55e", "Failed": "#ef4444"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
    )
    st.plotly_chart(fig, use_container_width=True, key="training_timeline")

    st.dataframe(df[["run_id", "model_name", "dataset", "previous_accuracy", "new_accuracy", "status", "timestamp"]].style.format({
        "previous_accuracy": "{:.2%}", "new_accuracy": "{:.2%}"
    }), use_container_width=True, hide_index=True)
