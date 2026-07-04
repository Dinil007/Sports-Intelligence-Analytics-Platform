"""Alert Center Dashboard Component."""
from __future__ import annotations

import streamlit as st
from services.monitoring_service import list_active_alerts

def render_alert_center() -> None:
    """Render active warning and critical system issues."""
    st.markdown("### 🚨 Active Alerts")
    alerts = list_active_alerts()
    
    if not alerts:
        st.success("No active issues detected.")
        return
        
    for alert in alerts:
        # Determine border color based on alert level
        color = "#ef4444" if alert["level"] == "CRITICAL" else "#f59e0b"
        bg_opacity = "rgba(239, 68, 68, 0.08)" if alert["level"] == "CRITICAL" else "rgba(245, 158, 11, 0.06)"
        
        st.markdown(
            f"""
            <div style="background:{bg_opacity}; border-left: 5px solid {color}; border-radius: 6px; padding: 12px 18px; margin-bottom: 12px;">
                <div style="font-weight: 800; font-size: 1.05rem; color: #f8fafc;">
                    {alert['title']} <span style="font-size: 0.72rem; padding: 2px 6px; border-radius: 4px; background: {color}; color: white; margin-left: 8px;">{alert['level']}</span>
                </div>
                <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">{alert['description']}</div>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 6px;">Triggered at: {alert['raised_at']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
