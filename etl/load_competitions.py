import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# StatsBomb competitions file
file_path = BASE_DIR / "data" / "raw" / "competitions.json"

# Load data
df = pd.read_json(file_path)

print("=" * 60)
print("SPORTS INTELLIGENCE & ANALYTICS PLATFORM")
print("Competitions Dataset")
print("=" * 60)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print(f"\nTotal competitions: {len(df)}")