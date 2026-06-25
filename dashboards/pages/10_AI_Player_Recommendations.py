import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from database.db_connection import engine

# Page Config handled by central entry point app.py

st.title("🔄 AI Transfer Recommendations")

players = pd.read_sql(
    """
    SELECT DISTINCT player_name
    FROM vw_scouting
    ORDER BY player_name;
    """,
    engine
)["player_name"].tolist()

selected_player = st.selectbox(
    "Choose a player",
    players
)

if st.button("Find Similar Players"):

    query = f"""
    SELECT *
    FROM vw_scouting
    WHERE player_name <> '{selected_player}'
    ORDER BY sporta_score DESC
    LIMIT 10;
    """

    df = pd.read_sql(query, engine)

    st.subheader("Recommended Players")
    st.dataframe(df, use_container_width=True)