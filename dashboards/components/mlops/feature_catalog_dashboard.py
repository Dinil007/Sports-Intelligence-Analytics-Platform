"""MLOps Feature Catalog Dashboard Component."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from services.mlops_service import list_features


def render_feature_catalog() -> None:
    """Render browsable feature catalog."""
    st.markdown("### 📖 Feature Catalog")

    features = list_features()
    if not features:
        st.info("No features in the catalog.")
        return

    df = pd.DataFrame(features)

    # ── Search / filter ───────────────────────────────────────────────────────
    search = st.text_input("🔍 Search features", key="catalog_search")
    if search:
        mask = df.apply(lambda row: search.lower() in str(row.values).lower(), axis=1)
        df = df[mask]

    st.dataframe(
        df[["name", "entity", "value_type", "description", "created_at"]],
        use_container_width=True, hide_index=True,
    )
    st.caption(f"{len(df)} feature(s) found")
