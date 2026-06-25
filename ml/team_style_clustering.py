import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

query = """
SELECT
    team_name,
    goals,
    total_xg,
    total_shots
FROM vw_team_performance
"""

df = pd.read_sql(query, engine)

features = ["goals", "total_xg", "total_shots"]

scaler = StandardScaler()
X = scaler.fit_transform(df[features])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

style_map = {
    0: "Attacking",
    1: "Balanced",
    2: "Defensive",
    3: "High Press"
}

df["playing_style"] = df["cluster"].map(style_map)

print(df[["team_name", "playing_style"]].sort_values("team_name"))