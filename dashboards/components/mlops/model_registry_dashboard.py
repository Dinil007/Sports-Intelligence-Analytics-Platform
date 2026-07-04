"""MLOps Model Registry Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.mlops_service import (
    deploy_model, list_registered_models, promote_model,
    register_model, rollback_deployment,
)
from mlops.constants import VALID_STAGES


_STAGE_COLORS = {
    "Development": "#64748b",
    "Testing":     "#f59e0b",
    "Staging":     "#3b82f6",
    "Production":  "#22c55e",
    "Archived":    "#94a3b8",
    "Rollback":    "#ef4444",
}


def render_model_registry_dashboard() -> None:
    """Render the model registry lifecycle panel."""
    st.markdown("### 🗂 Model Registry")

    models = list_registered_models()
    if not models:
        st.info("No models registered yet.")
    else:
        df = pd.DataFrame(models)

        # Stage distribution chart
        stage_counts = df["stage"].value_counts().reset_index()
        stage_counts.columns = ["stage", "count"]
        fig = px.bar(
            stage_counts, x="stage", y="count",
            title="Models by Lifecycle Stage",
            color="stage",
            color_discrete_map=_STAGE_COLORS,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_color="#f8fafc",
            showlegend=False,
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
        )
        st.plotly_chart(fig, use_container_width=True, key="registry_stage_bar")

        st.dataframe(df[["model_id", "name", "version", "stage", "registered_at"]],
                     use_container_width=True, hide_index=True)

    st.divider()

    # ── Register new model ────────────────────────────────────────────────────
    with st.expander("➕ Register New Model"):
        with st.form("register_model_form"):
            rc1, rc2 = st.columns(2)
            mid  = rc1.text_input("Model ID",      value="new_model")
            name = rc2.text_input("Name",           value="New Model")
            ver  = rc1.text_input("Version",        value="1.0.0")
            desc = rc2.text_input("Description",    value="")
            if st.form_submit_button("Register"):
                register_model(mid, name, ver, desc)
                st.success(f"Model `{mid}` registered.")
                st.rerun()

    # ── Promote model ─────────────────────────────────────────────────────────
    models_now = list_registered_models()
    if models_now:
        with st.expander("🚀 Promote / Transition Stage"):
            with st.form("promote_model_form"):
                pc1, pc2 = st.columns(2)
                sel_id    = pc1.selectbox("Model", [m["model_id"] for m in models_now], key="promo_sel")
                tgt_stage = pc2.selectbox("Target Stage", sorted(VALID_STAGES), key="promo_stage")
                if st.form_submit_button("Promote"):
                    promote_model(sel_id, tgt_stage)
                    st.success(f"Model `{sel_id}` promoted to `{tgt_stage}`.")
                    st.rerun()
