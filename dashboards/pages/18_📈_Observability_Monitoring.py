"""SPORTA VISTA PRO — Observability & Monitoring Platform Page (Phase 11).

Entry point delegating rendering to the monitoring dashboard component.
"""
from __future__ import annotations

import streamlit as st
from dashboards.components.monitoring.monitoring_dashboard import render_monitoring_dashboard

render_monitoring_dashboard()
