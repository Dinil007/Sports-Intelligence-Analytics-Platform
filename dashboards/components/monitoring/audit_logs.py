"""Audit Logs Dashboard Component."""
from __future__ import annotations

import pandas as pd
import streamlit as st
from services.monitoring_service import get_audit_logs

def render_audit_logs() -> None:
    """Render a timeline table of all user and system logs."""
    st.markdown("### 📋 System Audit Logs")
    logs = get_audit_logs()
    
    if not logs:
        st.info("No audit logs found.")
        return
        
    df = pd.DataFrame(logs)
    
    # We display them in a clean table representation
    st.dataframe(
        df[["timestamp", "user", "action", "status", "ip_address"]],
        use_container_width=True,
        hide_index=True
    )
