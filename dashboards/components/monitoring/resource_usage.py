"""Resource Usage Dashboard Component."""
from __future__ import annotations

import streamlit as st
from services.monitoring_service import get_resource_usage

def render_resource_usage() -> None:
    """Render system resource usage metrics details."""
    st.markdown("### 📊 Resource Usage")
    usage = get_resource_usage()
    
    cpu = usage["cpu"]
    mem = usage["memory"]
    disk = usage["disk"]
    uptime = usage["uptime"]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CPU Load", f"{cpu['percentage']}%", delta=cpu["status"])
    c2.metric("Memory Load", f"{mem['percentage']}%", delta=mem["status"])
    c3.metric("Disk Load", f"{disk['percentage']}%", delta=disk["status"])
    c4.metric("System Uptime", uptime["formatted"])
