import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

lineups_dir = Path(__file__).resolve().parent.parent / "data" / "raw" / "lineups"

players = {}

for file in lineups_dir.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        teams = json.load(f)

    for team in teams:
        for player in team.get("lineup", []):
            pid = player.get("player_id")
            if pid not in players:
                players[pid] = {
                    "player_id": pid,
                    "player_name": player.get("player_name"),
                    "nickname": player.get("player_nickname"),
                    "jersey_number": player.get("jersey_number"),
                    "country_name": player.get("country", {}).get("name"),
                }

df = pd.DataFrame(players.values())

df.to_sql(
    "dim_players",
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

print(f"✅ Loaded {len(df)} unique players into dim_players")