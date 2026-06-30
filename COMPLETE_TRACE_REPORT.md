# COMPLETE EVENT TRACE THROUGH PIPELINE

## Event Selected: Pass Event (549567bd-36de-4ac8-b8dc-6b5d3f1e4be8)
Match: 15946 (Barcelona vs Deportivo Alavés)
Minute: 0
Player: Jonathan Rodríguez Menéndez

---

## 1. RAW STATSBOMB JSON
```
Location: [61.0, 40.1]
pass_end_location: [None] (actually None in raw JSON)
```
✅ Coordinates PRESENT in source data

---

## 2. POSTGRESQL QUERY
```
id: 549567bd-36de-4ac8-b8dc-6b5d3f1e4be8
event_type: Pass
location_x: 61.0
location_y: 40.1
pass_end_x: 33.8
pass_end_y: 28.0
```
✅ Coordinates PRESENT in database

---

## 3. fetch_match_events() RETURN VALUE
```
Keys: ['ball_receipt_location', 'block_location', 'carry_end_location', 'clearance_location', 'event_type', 'id', 'interception_location', 'location', 'match_id', 'minute', 'pass_end_location', 'period', 'play_pattern', 'player_id', 'player_name', 'possession', 'pressure_location', 'second', 'shot_end_location', 'team_id', 'team_name']

event_type: Pass
location: [61.0, 40.1]  ← ✅ List format
type(location): <class 'list'>
pass_end_location: [33.8, 28.0]  ← ✅ converted by SQL CASE
```
✅ Coordinates PRESENT after repository layer

---

## 4. get_match_dashboard()["events"] 
```
Total events: 3762
Target event FOUND
event_type: Pass
location: [61.0, 40.1]  ← ✅ Still present
type(location): <class 'list'>
pass_end_location: [33.8, 28.0]  ← ✅ Still present
```
✅ Coordinates PRESENT in dashboard dict

---

## 5. WHAT pitch_dashboard.py RECEIVES
```
dash_events = match_dashboard.get("events", [])
# dash_events contains 3762 events with location data present
```
✅ Coordinates PRESENT when passed to pitch_dashboard

---

## 6. VERDICT: Coordinates DON'T disappear in this match

For match 15946 (with coordinates):
- All filter options EXCEPT "Tackle" would render visualizations
- "Tackle" would show: "No events available for pitch visualizations."

---

## THE REAL PROBLEM: Matches with NULL Coordinates

Testing match 4020846 (England Women's vs Spain Women's):

### PostgreSQL Query:
```
location_x=None, location_y=None
pass_end_x=None, pass_end_y=None
```
❌ Coordinates MISSING in database

### fetch_match_events() RETURN VALUE:
```
event_type: Pass
location: None  ← ❌ Set to None by SQL CASE
pass_end_location: None  ← ❌ Set to None by SQL CASE
```
❌ Coordinates MISSING after repository layer

### get_match_dashboard()["events"]:
```
event_type: Pass
location: None  ← ❌ Still None
pass_end_location: None  ← ❌ Still None
```
❌ Coordinates MISSING in dashboard dict

### What pitch_dashboard.py receives:
```python
events = match_dashboard.get("events", [])  # All events have location=None

for event_type in filters:
    filtered = [e for e in events if e.get("event_type") == target_type]
    has_any_coordinates = any(
        e.get("location") is not None or (
            e.get("pass_end_location") is not None
            or e.get("carry_end_location") is not None
            or e.get("shot_end_location") is not None
        )
        for e in filtered
    )
    
    if not has_any_coordinates:
        st.info("Pitch coordinates are unavailable for this event type.")  ← ⚠️ TRIGGERED
```

---

## ROOT CAUSE IDENTIFIED

### File: `database/match_repository.py`
### Function: `fetch_match_events(match_id)`
### Lines: 90-94 and 96-99

The SQL query uses CASE statements that return ARRAY only when BOTH coordinates are NOT NULL:

```sql
CASE
    WHEN location_x IS NOT NULL AND location_y IS NOT NULL
    THEN ARRAY[location_x, location_y]
    ELSE NULL
END AS location,
```

If ONLY ONE of location_x/location_y is NULL, the entire `location` field becomes NULL.
If BOTH are NULL (which is the case for women's matches), `location` is also NULL.

### Why coordinates are NULL in PostgreSQL for some matches:
**The ETL/ingestion process did NOT populate location_x and location_y columns for women's match data.**

---

## EXACT CAUSE OF "Pitch coordinates are unavailable"

1. **PostgreSQL fact_match_events table** has NULL values for location_x, location_y, pass_end_x, pass_end_y for certain matches (e.g., women's matches)

2. **SQL query in fetch_match_events()** (database/match_repository.py, lines 90-99) uses:
   ```sql
   CASE WHEN location_x IS NOT NULL AND location_y IS NOT NULL 
        THEN ARRAY[location_x, location_y] 
        ELSE NULL 
   END AS location
   ```
   
3. When coordinates are NULL in PostgreSQL, the CASE returns NULL

4. **get_match_dashboard()** passes these NULL locations through unchanged (no transformation)

5. **pitch_dashboard.py**, line 109-116:
   ```python
   has_any_coordinates = any(
       e.get("location") is not None or (
           e.get("pass_end_location") is not None
           or e.get("carry_end_location") is not None
           or e.get("shot_end_location") is not None
       )
       for e in filtered_events
   )
   ```
   
   When ALL events have location=None, this evaluates to False

6. **pitch_dashboard.py**, line 118-120:
   ```python
   if not has_any_coordinates:
       st.info("Pitch coordinates are unavailable for this event type.")
   ```
   This message is displayed

---

## SUMMARY

**The coordinates disappear at:**
- **File:** `database/match_repository.py`  
- **Function:** `fetch_match_events(match_id)`  
- **Lines:** 90-94 (location), 96-99 (pass_end_location), and similar for other location fields
- **Root cause:** The actual data in PostgreSQL `fact_match_events` table has NULL values for location columns for certain matches
- **User sees message:** Because the SQL CASE converts NULL coordinates to NULL arrays, which then fail the coordinate check in pitch_dashboard.py

**This is NOT a bug in the visualization code - it's a data availability issue.**
**The visualization code correctly handles missing data and shows an informative message.**
