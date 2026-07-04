"""Streaming Monitor Dashboard Component."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from services.monitoring_service import get_streaming_health, get_kafka_metrics, get_consumer_metrics, get_producer_metrics

def render_streaming_monitor() -> None:
    """Render Kafka broker, consumer groups, lag trends, and producer health."""
    st.markdown("### 🌪 Streaming Monitoring")
    health = get_streaming_health()
    kafka = get_kafka_metrics()
    consumers = get_consumer_metrics()
    producers = get_producer_metrics()
    
    broker = kafka["broker"]
    st.markdown(f"**Kafka Stream Broker:** `{broker['status']}` | **Cluster size:** `{broker['brokers_count']} nodes` | **Active controllers:** `{broker['active_controllers']}` | **Current Throughput:** `{broker['throughput_mb_sec']} MB/s` ")
    
    c1, c2 = st.columns(2)
    
    # Throughput history Line chart
    df_tp = pd.DataFrame(kafka["throughput_history"])
    fig_tp = px.line(
        df_tp, x="hour", y="throughput_mb_sec",
        title="Broker Throughput trends (MB/s)",
        color_discrete_sequence=["#fb923c"],
    )
    fig_tp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c1.plotly_chart(fig_tp, use_container_width=True, key="stream_tp_line")
    
    # Consumer lag Line chart
    df_lag = pd.DataFrame(consumers["lag_trends"])
    fig_lag = px.line(
        df_lag, x="hour", y="consumer_lag",
        title="Total Consumer Groups Lag (Messages)",
        color_discrete_sequence=["#ef4444"],
    )
    fig_lag.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", title_font_color="#f8fafc",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.12)"),
    )
    c2.plotly_chart(fig_lag, use_container_width=True, key="stream_lag_line")
    
    # Consumer status table
    st.markdown("#### Consumer Groups & Producer Health")
    tc1, tc2 = st.columns(2)
    tc1.write("**Consumer Groups**")
    tc1.dataframe(pd.DataFrame(consumers["groups"]), use_container_width=True, hide_index=True)
    tc2.write("**Producers Status**")
    tc2.dataframe(pd.DataFrame(producers), use_container_width=True, hide_index=True)
