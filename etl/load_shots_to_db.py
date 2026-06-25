import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

events_dir = Path(__file__).resolve().parent.parent / "data" / "raw" / "events"

total_shots = 0

for event_file in events_dir.glob("*.json"):
    match_id = int(event_file.stem)

    with open(event_file, "r", encoding="utf-8") as f:
        events = json.load(f)

    shot_rows = []

    for event in events:
        if event.get("type", {}).get("name") != "Shot":
            continue

        shot = event.get("shot", {})

        shot_rows.append({
    "id": str(event.get("id")),
    "match_id": match_id,
    "player_id": event.get("player", {}).get("id"),
    "player_name": event.get("player", {}).get("name"),
    "team_name": event.get("team", {}).get("name"),
    "minute": event.get("minute"),
    "shot_outcome": shot.get("outcome", {}).get("name"),
    "shot_first_time": shot.get("first_time"),
    "shot_one_on_one": shot.get("one_on_one"),
    "shot_open_goal": shot.get("open_goal"),
    "shot_statsbomb_xg": shot.get("statsbomb_xg"),
    "shot_x": event.get("location", [None, None])[0],
    "shot_y": event.get("location", [None, None])[1],
})
    if shot_rows:
        df = pd.DataFrame(shot_rows)
        df.to_sql(
            "fact_shots",
            engine,
            if_exists="append",
            index=False,
            method="multi",
        )
        total_shots += len(df)

print(f"✅ Loaded {total_shots} shots into fact_shots")