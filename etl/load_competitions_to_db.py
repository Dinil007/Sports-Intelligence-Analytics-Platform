import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Database connection
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

# Read StatsBomb competitions file
base_dir = Path(__file__).resolve().parent.parent
file_path = base_dir / "data" / "raw" / "competitions.json"

df = pd.read_json(file_path)

# Load into PostgreSQL
df.to_sql(
    "competitions_raw",
    engine,
    if_exists="replace",
    index=False
)

print("✅ competitions_raw table loaded successfully!")
print(f"Rows inserted: {len(df)}")