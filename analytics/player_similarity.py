import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
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

similarity_matrix = cosine_similarity(X)

player_name = input("Enter player name: ")

if player_name not in df["player_name"].values:
    print("Player not found.")
    exit()

idx = df[df["player_name"] == player_name].index[0]

scores = similarity_matrix[idx]

similar_players = (
    pd.DataFrame({
        "player_name": df["player_name"],
        "similarity": scores
    })
    .sort_values("similarity", ascending=False)
    .iloc[1:11]
)

print("\nTop Similar Players:\n")
print(similar_players)