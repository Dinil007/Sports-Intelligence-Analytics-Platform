import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

query = """
SELECT
    player_name,
    sporta_score,
    shots,
    passes,
    carries,
    pressures,
    recoveries,
    dribbles
FROM vw_sporta_score
ORDER BY sporta_score DESC
LIMIT 20;
"""

df = pd.read_sql(query, engine)

print(df)