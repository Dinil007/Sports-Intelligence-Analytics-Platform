import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

# --------------------------------------------------
# Events folder
# --------------------------------------------------
events_dir = Path(__file__).resolve().parent.parent / "data" / "raw" / "events"

updated = 0

# --------------------------------------------------
# Update coordinates
# --------------------------------------------------
with engine.begin() as conn:

    for event_file in events_dir.glob("*.json"):

        print(f"📂 Processing {event_file.name}")

        with open(event_file, "r", encoding="utf-8") as f:
            events = json.load(f)

        for event in events:

            if event.get("type", {}).get("name") != "Shot":
                continue

            location = event.get("location", [])

            shot_x = None
            shot_y = None

            if len(location) >= 2:
                shot_x = location[0]
                shot_y = location[1]

            conn.execute(
                text("""
                    UPDATE fact_shots
                    SET
                        shot_x = :shot_x,
                        shot_y = :shot_y
                    WHERE id = :id
                """),
                {
                    "id": str(event.get("id")),
                    "shot_x": shot_x,
                    "shot_y": shot_y
                }
            )

            updated += 1

print()
print("===================================")
print(f"✅ Finished successfully!")
print(f"✅ Updated coordinates for {updated} shots.")
print("===================================")