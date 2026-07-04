"""MLOps Deployment Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.mlops_service import deploy_model, rollback_deployment, list_registered_models
from mlops.registry.deployment_registry import DeploymentRegistry
from mlops.constants import VALID_STAGES


def render_deployment_dashboard() -> None:
    """Render deployment management UI."""
    st.markdown("### 🚢 Deployment Manager")

    models = list_registered_models()
    if not models:
        st.info("No models registered. Register models first.")
        return

    col1, col2 = st.columns(2)
    with col1:
        with st.form("deploy_form"):
            st.markdown("**Deploy Model**")
            dc1, dc2 = st.columns(2)
            model_id = dc1.selectbox("Model", [m["model_id"] for m in models], key="deploy_model")
            version  = dc2.text_input("Version", value="1.0.0", key="deploy_ver")
            stage    = st.selectbox("Target Stage", sorted(VALID_STAGES - {"Rollback"}), key="deploy_stage")
            if st.form_submit_button("🚀 Deploy"):
                result = deploy_model(model_id, version, stage)
                st.success(f"Deployed `{model_id}` v{version} → `{stage}`  Status: `{result['status']}`")
                st.rerun()

    with col2:
        with st.form("rollback_form"):
            st.markdown("**Rollback Deployment**")
            rb1, rb2 = st.columns(2)
            rb_model   = rb1.selectbox("Model",            [m["model_id"] for m in models], key="rollback_model")
            rb_version = rb2.text_input("Rollback Version", value="0.9.0", key="rollback_ver")
            if st.form_submit_button("⏪ Rollback"):
                result = rollback_deployment(rb_model, rb_version)
                st.warning(f"Rolled back `{rb_model}` to v{rb_version}. Status: `{result['status']}`")
                st.rerun()

    st.divider()
    render_deployment_history()


def render_deployment_history() -> None:
    """Render deployment event history timeline."""
    st.markdown("### 🗓 Deployment History")

    history = DeploymentRegistry().get_history()
    if not history:
        st.info("No deployments recorded yet.")
        return

    df = pd.DataFrame(history)

    fig = px.timeline(
        df.assign(start=df["timestamp"], end=df["timestamp"]),
        x_start="start", x_end="end",
        y="model_id",
        color="stage",
        title="Deployment Event Timeline",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
    )
    st.plotly_chart(fig, use_container_width=True, key="deploy_timeline")

    st.dataframe(
        df[["model_id", "version", "stage", "status", "timestamp"]],
        use_container_width=True, hide_index=True,
    )
