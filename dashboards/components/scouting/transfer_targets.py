from __future__ import annotations

import pandas as pd
import streamlit as st

from services.scouting_service import generate_transfer_targets


def render_transfer_targets() -> None:
    st.header("Transfer Targets")
    targets = generate_transfer_targets()
    tabs = st.tabs(["High Priority", "Medium Priority", "Low Priority"])
    keys = ["high_priority", "medium_priority", "low_priority"]
    for tab, key in zip(tabs, keys):
        with tab:
            rows = targets.get(key, [])
            if rows:
                st.dataframe(pd.DataFrame(rows)[["player_name", "club", "position", "age", "recruitment_score", "sporta_score"]], use_container_width=True, hide_index=True)
            else:
                st.info("No players in this priority band.")
