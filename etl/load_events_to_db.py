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

events_dir = Path(__file__).resolve().parent.parent / "data" / "raw" / "events"

total_rows = 0
first_file = True

for event_file in events_dir.glob("*.json"):
    print(f"Processing {event_file.name}...")

    with open(event_file, "r", encoding="utf-8") as f:
        events = json.load(f)

    rows = []

    match_id = int(event_file.stem)

    for e in events:
        rows.append({
            "id": str(e.get("id")),
            "match_id": match_id,
            "minute": e.get("minute"),
            "second": e.get("second"),
            "period": e.get("period"),
            "event_type": e.get("type", {}).get("name"),
            "player_id": e.get("player", {}).get("id"),
            "player_name": e.get("player", {}).get("name"),
            "team_id": e.get("team", {}).get("id"),
            "team_name": e.get("team", {}).get("name"),
            "possession": e.get("possession"),
            "play_pattern": e.get("play_pattern", {}).get("name"),
        })

    df = pd.DataFrame(rows)

    df.to_sql(
        "fact_match_events",
        engine,
        if_exists="append" if not first_file else "replace",
        index=False,
        method="multi",
    )

    first_file = False
    total_rows += len(df)

print(f"\n✅ Total events loaded: {total_rows}")