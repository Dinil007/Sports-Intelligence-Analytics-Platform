import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

# Auth guard
from auth.streamlit_auth import is_authenticated
if not is_authenticated():
    st.stop()

# Original page content continues below...
st.title("🔍 Scouting")
