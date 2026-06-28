"""Action buttons for recommendation cards.

Buttons emit placeholder events only. No navigation logic is implemented here.
"""

from __future__ import annotations

import streamlit as st


def render_action_buttons(player_name: str) -> None:
    """
    Render action buttons using native Streamlit components.

    Parameters
    ----------
    player_name : str
        The player name used to generate unique keys for each button.
    """
    safe_key = player_name.replace(" ", "_").replace(".", "")
    buttons = [
        "Compare Player",
        "View Profile",
        "Export PDF",
    ]

    cols = st.columns(len(buttons))
    for i, label in enumerate(buttons):
        action_key = f"{label.lower().replace(' ', '_')}_{safe_key}"
        with cols[i]:
            st.button(
                label,
                key=action_key,
                use_container_width=True,
            )
