from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import generate_transfer_shortlist


def render_transfer_shortlist() -> None:
    st.header("Transfer Shortlist")
    shortlist = generate_transfer_shortlist(limit=25)
    if not shortlist:
        st.warning("No shortlist candidates available.")
        return
    st.dataframe(pd.DataFrame(shortlist)[["player_name", "club", "position", "age", "minutes", "sporta_score", "recruitment_score", "market_value"]], use_container_width=True, hide_index=True)
