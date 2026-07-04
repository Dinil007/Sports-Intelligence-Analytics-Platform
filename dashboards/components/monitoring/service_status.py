"""Service Status Dashboard Component."""
from __future__ import annotations

import pandas as pd
import streamlit as st
from services.monitoring_service import get_service_status

def render_service_status() -> None:
    """Render dependent platform services status table."""
    st.markdown("### 🧱 Platform Service Status")
    services = get_service_status()
    
    df = pd.DataFrame(services)
    st.dataframe(df, use_container_width=True, hide_index=True)
