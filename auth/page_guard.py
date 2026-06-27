"""Universal page-level auth guard for all Streamlit pages.

Uses `st.stop()` to halt rendering for unauthenticated users.
The outer navigation in `dashboards/app.py` controls which pages
are visible; individual pages only need a defensive gate.
"""

import streamlit as st


def require_auth() -> None:
    """
    Stop page execution if user is not authenticated.
    The outer navigation in `dashboards/app.py` already ensures
    unauthenticated users only see the login screen; this is a
    defensive guard for direct page access.
    """
    if not (st.session_state.get("authenticated") and st.session_state.get("role")):
        st.stop()
