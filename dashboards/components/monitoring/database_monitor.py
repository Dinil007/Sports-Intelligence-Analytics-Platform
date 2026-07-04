"""Database Monitor Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from services.monitoring_service import get_database_health, get_database_connections, get_database_storage

def render_database_monitor() -> None:
    """Render database connections, storage usage, and slow query logs."""
    st.markdown("### 💾 Database Monitoring")
    health = get_database_health()
    conn_data = get_database_connections()
    storage = get_database_storage()
    
    st.markdown(f"**Database Status:** `{health['status']}` | **Cache Hit Rate:** `{health['cache_hit_rate_percent']}%` | **Read/Write Ratio:** `{health['read_write_ratio']}`")
    
    c1, c2 = st.columns(2)
    
    # DB Connections Line chart
    df_conn = pd.DataFrame(conn_data["history"])
    fig_conn = px.line(
        df_conn, x="hour", y="active_connections",
        title="Active Connection Pool Usage",
        color_discrete_sequence=["#34d399"],
    )
    fig_conn.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c1.plotly_chart(fig_conn, use_container_width=True, key="db_conn_line")
    
    # DB size gauge
    db_size = storage["size_gb"]
    fig_size = go.Figure(go.Indicator(
        mode="gauge+number",
        value=db_size,
        title={"text": "Database Size (GB)", "font": {"color": "#f8fafc", "size": 14}},
        number={"suffix": " GB", "font": {"color": "#f8fafc", "size": 22}},
        gauge={
            "axis": {"range": [0, 50], "tickcolor": "#64748b"},
            "bar": {"color": "#10b981"},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, 30], "color": "rgba(16,185,129,0.1)"},
                {"range": [30, 45], "color": "rgba(245,158,11,0.18)"},
                {"range": [45, 50], "color": "rgba(239,68,68,0.22)"},
            ]
        }
    ))
    fig_size.update_layout(
        height=220, margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
    )
    c2.plotly_chart(fig_size, use_container_width=True, key="db_size_gauge")
    
    # Slow Query Log
    st.markdown("#### Slow Query Log Highlights")
    st.dataframe(pd.DataFrame(conn_data["slow_queries"]), use_container_width=True, hide_index=True)
