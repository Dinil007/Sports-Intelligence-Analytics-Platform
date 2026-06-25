import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

matches_dir = Path(__file__).resolve().parent.parent / "data" / "raw" / "matches"

rows = []

for competition_folder in matches_dir.iterdir():
    if competition_folder.is_dir():
        for file in competition_folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                matches = json.load(f)

            for m in matches:
                rows.append({
                    "match_id": m.get("match_id"),
                    "match_date": m.get("match_date"),
                    "kick_off": m.get("kick_off"),
                    "home_score": m.get("home_score"),
                    "away_score": m.get("away_score"),

                    "competition_id": m.get("competition", {}).get("competition_id"),
                    "competition_name": m.get("competition", {}).get("competition_name"),

                    "season_id": m.get("season", {}).get("season_id"),
                    "season_name": m.get("season", {}).get("season_name"),

                    "home_team_id": m.get("home_team", {}).get("home_team_id"),
                    "home_team_name": m.get("home_team", {}).get("home_team_name"),

                    "away_team_id": m.get("away_team", {}).get("away_team_id"),
                    "away_team_name": m.get("away_team", {}).get("away_team_name"),
                })

df = pd.DataFrame(rows)

df.to_sql(
    "matches_raw",
    engine,
    if_exists="replace",
    index=False
)

print(f"✅ Loaded {len(df)} matches into PostgreSQL!")