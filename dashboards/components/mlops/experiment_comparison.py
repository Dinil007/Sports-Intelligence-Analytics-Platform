"""MLOps Experiment Comparison Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.mlops_service import compare_experiments, list_experiments


def render_experiment_comparison() -> None:
    """Render experiment comparison section."""
    st.markdown("### 🔬 Experiment Comparison")

    all_exps = list_experiments()
    if not all_exps:
        st.info("No experiments available for comparison.")
        return

    ids = [e["experiment_id"] for e in all_exps]
    selected = st.multiselect("Select experiments to compare", ids, default=ids[:min(2, len(ids))],
                              key="exp_compare_select")

    if not selected:
        st.info("Select at least one experiment.")
        return

    compared = compare_experiments(selected)
    df = pd.DataFrame(compared)

    metrics = ["accuracy", "precision", "recall", "f1"]
    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Bar(
            name=row["experiment_id"],
            x=metrics,
            y=[row[m] for m in metrics],
        ))

    fig.update_layout(
        title="Metric Comparison Across Experiments",
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        yaxis=dict(range=[0, 1], tickformat=".0%", gridcolor="rgba(148,163,184,0.12)"),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True, key="exp_compare_chart")

    st.dataframe(df[["experiment_id", "model_name", "algorithm"] + metrics].style.format(
        {m: "{:.2%}" for m in metrics}
    ), use_container_width=True, hide_index=True)
