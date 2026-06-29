import sys
from database.db_connection import engine
from sqlalchemy import text

print("importing done", flush=True)
with engine.connect() as c:
    print("DB_OK", c.execute(text("SELECT 1")).scalar(), flush=True)

from database.recommendation_repository import fetch_candidate_player_names
print("repo imported", flush=True)
names = fetch_candidate_player_names()
print("NAMES_COUNT", len(names), flush=True)
print("FIRST_NAMES", names[:5], flush=True)
