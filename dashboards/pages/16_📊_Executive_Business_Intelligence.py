"""Executive Business Intelligence & Club Management page."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from auth.streamlit_auth import is_authenticated
from dashboards.components.executive_bi.executive_dashboard import render_executive_dashboard

if not is_authenticated():
    st.stop()

render_executive_dashboard()
