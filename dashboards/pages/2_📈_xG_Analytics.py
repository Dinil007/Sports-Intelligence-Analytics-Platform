import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os

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

st.title("📈 Expected Goals (xG) Analytics")

query = """
SELECT
    player_name,
    goals,
    expected_goals,
    total_shots,
    goals_minus_xg
FROM vw_xg_analysis
ORDER BY expected_goals DESC
LIMIT 50;
"""

df = pd.read_sql(query, engine)

st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("🎯 Top Players by Expected Goals")

chart_df = df.set_index("player_name")[["expected_goals"]]
st.bar_chart(chart_df)