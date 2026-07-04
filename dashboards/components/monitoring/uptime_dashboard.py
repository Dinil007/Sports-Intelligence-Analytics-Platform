"""Uptime Dashboard Component."""
from __future__ import annotations

import streamlit as st
from services.monitoring_service import get_resource_usage

def render_uptime_dashboard() -> None:
    """Render uptime details metrics."""
    st.markdown("### ⏱ Service Uptime Details")
    usage = get_resource_usage()
    uptime = usage["uptime"]
    
    st.info(f"System Uptime is currently **{uptime['formatted']}**.")
