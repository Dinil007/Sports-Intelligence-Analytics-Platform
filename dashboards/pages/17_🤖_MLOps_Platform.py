"""SPORTA VISTA PRO — MLOps Platform Page (Phase 10).

Entry point delegating rendering to the MLOps dashboard component.
"""
from __future__ import annotations

import streamlit as st
from dashboards.components.mlops.mlops_dashboard import render_mlops_dashboard

render_mlops_dashboard()
