import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from database.db_connection import engine
from ai.response_generator import explain_results

# Page Config handled by central entry point app.py

st.title("📋 AI Scouting Report")

# Load player names
players = pd.read_sql(
    "SELECT DISTINCT player_name FROM vw_scouting ORDER BY player_name;",
    engine,
)["player_name"].tolist()

player = st.selectbox("Select a Player", players)

if st.button("Generate Report"):

    query = f"""
    SELECT *
    FROM vw_scouting
    WHERE player_name = '{player}';
    """

    df = pd.read_sql(query, engine)

    st.subheader("📊 Player Statistics")
    st.dataframe(df, use_container_width=True)

    report = explain_results(
        question=f"Generate a detailed scouting report for {player}",
        dataframe_text=df.to_string(index=False),
    )

    st.subheader("🤖 AI Scouting Report")
    st.write(report)