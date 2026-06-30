import json

with open('data/raw/events/4020846.json', encoding='utf-8') as f:
    data = json.load(f)

pass_events = [e for e in data if e.get('type', {}).get('name') == 'Pass']
print(f'Total Pass events: {len(pass_events)}')

bad_loc = [e for e in pass_events if e.get('location') is not None and len(e.get('location')) != 2]
bad_pass_end = [e for e in pass_events if e.get('pass', {}).get('end_location') is not None and len(e.get('pass', {}).get('end_location')) != 2]

print(f'Pass events with bad location length (!=2): {len(bad_loc)}')
print(f'Pass events with bad pass_end_location length (!=2): {len(bad_pass_end)}')

if bad_loc:
    print('\nSample bad location:')
    e = bad_loc[0]
    print(f'  id: {e.get("id")}')
    print(f'  location: {e.get("location")}')
    print(f'  location type: {type(e.get("location"))}')
    print(f'  location length: {len(e.get("location"))}')

if bad_pass_end:
    print('\nSample bad pass_end_location:')
    e = bad_pass_end[0]
    print(f'  id: {e.get("id")}')
    print(f'  pass.end_location: {e.get("pass", {}).get("end_location")}')
    print(f'  pass.end_location type: {type(e.get("pass", {}).get("end_location"))}')
    print(f'  pass.end_location length: {len(e.get("pass", {}).get("end_location"))}')

# Also check what the ETL stored in PostgreSQL
from database.match_repository import fetch_match_events
events = fetch_match_events(4020846)
pass_db = [e for e in events if e.get('event_type') == 'Pass']
print(f'\nPass events from DB: {len(pass_db)}')

# Check for any with wrong length
bad_db_loc = [e for e in pass_db if e.get('location') is not None and len(e.get('location')) != 2]
bad_db_pass_end = [e for e in pass_db if e.get('pass_end_location') is not None and len(e.get('pass_end_location')) != 2]
print(f'DB pass events with bad location length: {len(bad_db_loc)}')
print(f'DB pass events with bad pass_end_location length: {len(bad_db_pass_end)}')

if bad_db_loc:
    print('\nSample bad DB location:')
    e = bad_db_loc[0]
    print(f'  id: {e.get("id")}')
    print(f'  location: {e.get("location")}')
    print(f'  location length: {len(e.get("location"))}')

if bad_db_pass_end:
    print('\nSample bad DB pass_end_location:')
    e = bad_db_pass_end[0]
    print(f'  id: {e.get("id")}')
    print(f'  pass_end_location: {e.get("pass_end_location")}')
    print(f'  pass_end_location length: {len(e.get("pass_end_location"))}')
