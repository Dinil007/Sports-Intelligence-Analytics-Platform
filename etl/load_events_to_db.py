import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

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



def _ensure_coordinate_columns():
    """Add nullable coordinate columns if they are missing."""
    from sqlalchemy import inspect
    insp = inspect(engine)
    if not insp.has_table("fact_match_events"):
        return
    existing_cols = {c["name"] for c in insp.get_columns("fact_match_events")}
    new_cols = [
        ("location_x", "FLOAT"),
        ("location_y", "FLOAT"),
        ("pass_end_x", "FLOAT"),
        ("pass_end_y", "FLOAT"),
        ("carry_end_x", "FLOAT"),
        ("carry_end_y", "FLOAT"),
        ("shot_end_x", "FLOAT"),
        ("shot_end_y", "FLOAT"),
        ("shot_end_z", "FLOAT"),
        ("pressure_x", "FLOAT"),
        ("pressure_y", "FLOAT"),
        ("block_x", "FLOAT"),
        ("block_y", "FLOAT"),
        ("interception_x", "FLOAT"),
        ("interception_y", "FLOAT"),
        ("clearance_x", "FLOAT"),
        ("clearance_y", "FLOAT"),
        ("ball_receipt_x", "FLOAT"),
        ("ball_receipt_y", "FLOAT"),
    ]
    with engine.begin() as conn:
        for col_name, col_type in new_cols:
            if col_name not in existing_cols:
                conn.execute(
                    text(f"ALTER TABLE fact_match_events ADD COLUMN {col_name} {col_type}")
                )

_ensure_coordinate_columns()

for event_file in events_dir.glob("*.json"):
    print(f"Processing {event_file.name}...")

    with open(event_file, "r", encoding="utf-8") as f:
        events = json.load(f)

    rows = []

    match_id = int(event_file.stem)

    for e in events:
        loc = e.get("location")
        location_x = loc[0] if isinstance(loc, list) and len(loc) >= 1 else None
        location_y = loc[1] if isinstance(loc, list) and len(loc) >= 2 else None

        pass_end = e.get("pass", {}).get("end_location")
        pass_end_x = pass_end[0] if isinstance(pass_end, list) and len(pass_end) >= 1 else None
        pass_end_y = pass_end[1] if isinstance(pass_end, list) and len(pass_end) >= 2 else None

        carry_end = e.get("carry", {}).get("end_location")
        carry_end_x = carry_end[0] if isinstance(carry_end, list) and len(carry_end) >= 1 else None
        carry_end_y = carry_end[1] if isinstance(carry_end, list) and len(carry_end) >= 2 else None

        shot_end = e.get("shot", {}).get("end_location")
        if isinstance(shot_end, list) and len(shot_end) >= 3:
            shot_end_x, shot_end_y, shot_end_z = shot_end[0], shot_end[1], shot_end[2]
        elif isinstance(shot_end, list) and len(shot_end) == 2:
            shot_end_x, shot_end_y, shot_end_z = shot_end[0], shot_end[1], None
        else:
            shot_end_x = shot_end_y = shot_end_z = None

        ball_receipt_loc = e.get("ball_receipt", {}).get("location")
        ball_receipt_x = ball_receipt_loc[0] if isinstance(ball_receipt_loc, list) and len(ball_receipt_loc) >= 1 else None
        ball_receipt_y = ball_receipt_loc[1] if isinstance(ball_receipt_loc, list) and len(ball_receipt_loc) >= 2 else None

        pressure_loc = e.get("pressure", {}).get("location")
        pressure_x = pressure_loc[0] if isinstance(pressure_loc, list) and len(pressure_loc) >= 1 else None
        pressure_y = pressure_loc[1] if isinstance(pressure_loc, list) and len(pressure_loc) >= 2 else None

        block_loc = e.get("block", {}).get("location")
        block_x = block_loc[0] if isinstance(block_loc, list) and len(block_loc) >= 1 else None
        block_y = block_loc[1] if isinstance(block_loc, list) and len(block_loc) >= 2 else None

        interception_loc = e.get("interception", {}).get("location")
        interception_x = interception_loc[0] if isinstance(interception_loc, list) and len(interception_loc) >= 1 else None
        interception_y = interception_loc[1] if isinstance(interception_loc, list) and len(interception_loc) >= 2 else None

        clearance_loc = e.get("clearance", {}).get("location")
        clearance_x = clearance_loc[0] if isinstance(clearance_loc, list) and len(clearance_loc) >= 1 else None
        clearance_y = clearance_loc[1] if isinstance(clearance_loc, list) and len(clearance_loc) >= 2 else None

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
            "location_x": location_x,
            "location_y": location_y,
            "pass_end_x": pass_end_x,
            "pass_end_y": pass_end_y,
            "carry_end_x": carry_end_x,
            "carry_end_y": carry_end_y,
            "shot_end_x": shot_end_x,
            "shot_end_y": shot_end_y,
            "shot_end_z": shot_end_z,
            "pressure_x": pressure_x,
            "pressure_y": pressure_y,
            "block_x": block_x,
            "block_y": block_y,
            "interception_x": interception_x,
            "interception_y": interception_y,
            "clearance_x": clearance_x,
            "clearance_y": clearance_y,
            "ball_receipt_x": ball_receipt_x,
            "ball_receipt_y": ball_receipt_y,
        })

    df = pd.DataFrame(rows)

    df.to_sql(
        "fact_match_events",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    first_file = False
    total_rows += len(df)

print(f"\n✅ Total events loaded: {total_rows}")