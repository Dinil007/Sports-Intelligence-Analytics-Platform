import json

# Simulate the ETL extraction logic for match 4020846
with open('data/raw/events/4020846.json') as f:
    data = json.load(f)

print("Simulating ETL coordinate extraction for match 4020846:")
print(f"Total events in raw JSON: {len(data)}\n")

# Test the exact ETL logic (lines 74-86)
rows_with_coords = 0
rows_without_coords = 0
sample_with = None
sample_without = None

for e in data:
    loc = e.get("location")
    location_x = loc[0] if isinstance(loc, list) and len(loc) >= 1 else None
    location_y = loc[1] if isinstance(loc, list) and len(loc) >= 2 else None
    
    if location_x is not None and location_y is not None:
        rows_with_coords += 1
        if sample_with is None:
            sample_with = (e.get('id'), e.get('type', {}).get('name'), location_x, location_y)
    else:
        rows_without_coords += 1
        if sample_without is None:
            sample_without = (e.get('id'), e.get('type', {}).get('name'), location_x, location_y)

print(f"Events the ETL WOULD extract coordinates from: {rows_with_coords}")
print(f"Events the ETL would NOT extract coordinates from: {rows_without_coords}")
print(f"\nSample WITH coords: id={sample_with[0]}, type={sample_with[1]}, x={sample_with[2]}, y={sample_with[3]}")
print(f"Sample WITHOUT coords: id={sample_without[0]}, type={sample_without[1]}, x={sample_without[2]}, y={sample_without[3]}")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)
print(f"The ETL WOULD correctly extract location coordinates from {rows_with_coords} events.")
print(f"But PostgreSQL has 0 rows with location_x IS NOT NULL for match 4020846.")
print(f"\nThis means:")
print(f"  1. The ETL was run BEFORE the location columns existed in the table")
print(f"  OR")
print(f"  2. The ETL failed for this specific file")
print(f"  OR")
print(f"  3. The ETL used 'append' mode but the data was inserted without coordinates")
