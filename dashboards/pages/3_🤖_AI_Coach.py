import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os

from auth.streamlit_auth import is_authenticated
if not is_authenticated():
    st.stop()

# Load environment variables
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

import sys
# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

engine = create_engine(DATABASE_URL)

# Page Config handled by central entry point app.py

st.title("🤖 AI Coach Assistant")

question = st.text_input(
    "Ask a question",
    placeholder="Examples: top players, top scorers, team performance"
)

if question:
    q = question.lower().strip()

    if q == "top players":
        sql = """
        SELECT player_name, sporta_score
        FROM vw_sporta_score
        ORDER BY sporta_score DESC
        LIMIT 10;
        """
        st.dataframe(pd.read_sql(sql, engine), width="stretch")

    elif q == "top scorers":
        sql = """
        SELECT player_name, goals, total_xg
        FROM vw_top_goal_scorers
        ORDER BY goals DESC
        LIMIT 10;
        """
        st.dataframe(pd.read_sql(sql, engine), width="stretch")

    elif q == "team performance":
        sql = """
        SELECT team_name, goals, total_xg, total_shots
        FROM vw_team_performance
        ORDER BY goals DESC
        LIMIT 10;
        """
        st.dataframe(pd.read_sql(sql, engine), width="stretch")

    else:
        st.warning(
            "Currently supported: top players, top scorers, team performance"
        )