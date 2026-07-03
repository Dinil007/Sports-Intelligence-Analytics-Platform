from __future__ import annotations

import pandas as pd
import streamlit as st

from services.transfer_intelligence_service import calculate_transfer_targets


def render_transfer_targets() -> None:
    st.header("Transfer Targets")
    targets = calculate_transfer_targets()
    columns = ["Player", "Club", "Position", "Age", "SPORTA Score", "Market Value", "Contract Status", "Priority"]
    st.dataframe(pd.DataFrame(targets, columns=columns), use_container_width=True, hide_index=True)
