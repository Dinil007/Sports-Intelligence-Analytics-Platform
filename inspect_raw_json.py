import json

# Check match 4020846 raw JSON
with open('data/raw/events/4020846.json') as f:
    data = json.load(f)

total = len(data)
with_loc = sum(1 for e in data if e.get('location') is not None)
without_loc = total - with_loc

sample_with = next((e for e in data if e.get('location') is not None), None)
sample_without = next((e for e in data if e.get('location') is None), None)

print('Match 4020846 raw JSON:')
print(f'  Total events: {total}')
print(f'  With location: {with_loc}')
print(f'  Without location: {without_loc}')

if sample_with:
    print(f'  Sample WITH location:')
    print(f'    id: {sample_with.get("id")}')
    print(f'    type: {sample_with.get("type", {}).get("name")}')
    print(f'    location: {sample_with.get("location")}')

if sample_without:
    print(f'  Sample WITHOUT location:')
    print(f'    id: {sample_without.get("id")}')
    print(f'    type: {sample_without.get("type", {}).get("name")}')
    print(f'    location: {sample_without.get("location")}')
