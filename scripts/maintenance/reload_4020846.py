"""Reload match 4020846 to fix missing coordinates."""
import json
import pandas as pd
from sqlalchemy import text
from database.db_connection import engine

event_file = 'data/raw/events/4020846.json'
print(f'Loading {event_file}...')
with open(event_file, 'r', encoding='utf-8') as f:
    events = json.load(f)

rows = []
match_id = 4020846
print(f'Processing {len(events)} events...')

for e in events:
    loc = e.get('location')
    location_x = loc[0] if isinstance(loc, list) and len(loc) >= 1 else None
    location_y = loc[1] if isinstance(loc, list) and len(loc) >= 2 else None
    
    pass_end = e.get('pass', {}).get('end_location')
    pass_end_x = pass_end[0] if isinstance(pass_end, list) and len(pass_end) >= 1 else None
    pass_end_y = pass_end[1] if isinstance(pass_end, list) and len(pass_end) >= 2 else None
    
    carry_end = e.get('carry', {}).get('end_location')
    carry_end_x = carry_end[0] if isinstance(carry_end, list) and len(carry_end) >= 1 else None
    carry_end_y = carry_end[1] if isinstance(carry_end, list) and len(carry_end) >= 2 else None
    
    shot_end = e.get('shot', {}).get('end_location')
    if isinstance(shot_end, list) and len(shot_end) >= 3:
        shot_end_x, shot_end_y, shot_end_z = shot_end[0], shot_end[1], shot_end[2]
    elif isinstance(shot_end, list) and len(shot_end) == 2:
        shot_end_x, shot_end_y, shot_end_z = shot_end[0], shot_end[1], None
    else:
        shot_end_x = shot_end_y = shot_end_z = None
    
    rows.append({
        'id': str(e.get('id')),
        'match_id': match_id,
        'minute': e.get('minute'),
        'second': e.get('second'),
        'period': e.get('period'),
        'event_type': e.get('type', {}).get('name'),
        'player_id': e.get('player', {}).get('id'),
        'player_name': e.get('player', {}).get('name'),
        'team_id': e.get('team', {}).get('id'),
        'team_name': e.get('team', {}).get('name'),
        'possession': e.get('possession'),
        'play_pattern': e.get('play_pattern', {}).get('name'),
        'location_x': location_x,
        'location_y': location_y,
        'pass_end_x': pass_end_x,
        'pass_end_y': pass_end_y,
        'carry_end_x': carry_end_x,
        'carry_end_y': carry_end_y,
        'shot_end_x': shot_end_x,
        'shot_end_y': shot_end_y,
        'shot_end_z': shot_end_z,
    })

df = pd.DataFrame(rows)
print(f'Inserting {len(df)} rows...')
df.to_sql('fact_match_events', engine, if_exists='append', index=False, method='multi')
print(f'✅ Inserted {len(df)} rows for match 4020846')
