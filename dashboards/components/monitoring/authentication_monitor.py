"""Authentication Monitor Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from services.monitoring_service import get_authentication_statistics, get_login_statistics, get_session_statistics

def render_authentication_monitor() -> None:
    """Render user logins, session concurrency, and security logs."""
    st.markdown("### 🔐 Authentication Monitoring")
    auth_data = get_authentication_statistics()
    login_data = get_login_statistics()
    session_data = get_session_statistics()
    
    st.markdown(f"**Concurrently Active Sessions:** `{auth_data['sessions']['active_sessions']}` | **Average session time:** `{auth_data['sessions']['average_session_duration_minutes']} min` | **Failed logins (24h):** `{auth_data['login']['failed_attempts_24h']}`")
    
    c1, c2 = st.columns(2)
    
    # Login Trends Line chart
    df_logins = pd.DataFrame(login_data["trends"])
    fig_log = px.line(
        df_logins, x="hour", y="logins",
        title="User Logins Trend",
        color_discrete_sequence=["#e0f2fe"],
    )
    fig_log.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c1.plotly_chart(fig_log, use_container_width=True, key="auth_logins_line")
    
    # Active Sessions Area chart
    df_sessions = pd.DataFrame(session_data["trends"])
    fig_sess = px.area(
        df_sessions, x="hour", y="active_sessions",
        title="Concurrent Active User Sessions",
        color_discrete_sequence=["#38bdf8"],
    )
    fig_sess.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c2.plotly_chart(fig_sess, use_container_width=True, key="auth_sessions_area")
    
    # Security alerts log
    st.markdown("#### Security Log Events")
    st.dataframe(pd.DataFrame(auth_data["security_events"]), use_container_width=True, hide_index=True)
