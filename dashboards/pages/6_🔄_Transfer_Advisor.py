import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
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

st.title("🔄 Transfer Recommendation Engine")

query = """
SELECT
    player_name,
    sporta_score,
    shots,
    passes,
    carries,
    dribbles,
    recoveries,
    pressures
FROM vw_sporta_score
"""

df = pd.read_sql(query, engine)

player = st.selectbox(
    "Select a player to replace",
    sorted(df["player_name"].tolist())
)

features = [
    "sporta_score",
    "shots",
    "passes",
    "carries",
    "dribbles",
    "recoveries",
    "pressures"
]

scaler = StandardScaler()
X = scaler.fit_transform(df[features])

similarity = cosine_similarity(X)

idx = df[df["player_name"] == player].index[0]

scores = similarity[idx]

recommendations = (
    pd.DataFrame({
        "player_name": df["player_name"],
        "similarity_score": scores
    })
    .sort_values("similarity_score", ascending=False)
    .iloc[1:11]
)

st.subheader("🎯 Recommended Replacements")
st.dataframe(
    recommendations,
    width="stretch",
    hide_index=True
)