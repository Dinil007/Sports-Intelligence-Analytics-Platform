"""MLOps Feature Store Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.mlops_service import create_feature, list_features, validate_feature


def render_feature_store_dashboard() -> None:
    """Render the feature store registration panel."""
    st.markdown("### 🗃 Feature Store")

    features = list_features()
    if not features:
        st.info("No features registered yet.")
    else:
        df = pd.DataFrame(features)

        c1, c2 = st.columns(2)
        c1.metric("Total Features", len(df))
        c2.metric("Entities", df["entity"].nunique() if "entity" in df.columns else 0)

        counts_df = df["entity"].value_counts().reset_index()
        counts_df.columns = ["entity", "feature_count"]
        fig = px.bar(
            counts_df,
            x="entity", y="feature_count",
            title="Features per Entity",
            color_discrete_sequence=["#a78bfa"],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_color="#f8fafc",
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
        )
        st.plotly_chart(fig, use_container_width=True, key="feature_entity_bar")
        st.dataframe(df[["name", "entity", "value_type", "description"]], use_container_width=True, hide_index=True)

    st.divider()

    with st.expander("➕ Register New Feature"):
        with st.form("register_feature_form"):
            fc1, fc2 = st.columns(2)
            fname  = fc1.text_input("Feature Name",  value="new_feature")
            entity = fc2.text_input("Entity",         value="player")
            vtype  = fc1.selectbox("Value Type",      ["float", "int", "bool", "str"])
            fdesc  = fc2.text_input("Description",    value="")
            if st.form_submit_button("Register Feature"):
                create_feature(fname, entity, vtype, fdesc)
                st.success(f"Feature `{fname}` registered.")
                st.rerun()

    with st.expander("✅ Validate Feature Value"):
        with st.form("validate_feature_form"):
            vf1, vf2 = st.columns(2)
            val_input = vf1.text_input("Value", value="5")
            val_type  = vf2.selectbox("Expected Type", ["float", "int", "bool", "str"], key="val_type")
            if st.form_submit_button("Validate"):
                ok = validate_feature(val_input, val_type)
                if ok:
                    st.success(f"`{val_input}` is a valid `{val_type}`.")
                else:
                    st.error(f"`{val_input}` is NOT a valid `{val_type}`.")
