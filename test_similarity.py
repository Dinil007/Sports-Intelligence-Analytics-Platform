import pandas as pd
from database.db_connection import engine
from ml.player_similarity import get_similar_players

# Show available players
players = pd.read_sql(
    """
    SELECT DISTINCT player_name
    FROM vw_scouting
    ORDER BY player_name
    LIMIT 20;
    """,
    engine,
)

print("\n===== First 20 Players in Database =====")
print(players)

# Ask user for a player name
player_name = input("\nEnter player name (or part of the name): ").strip()

# Get similar players
result = get_similar_players(player_name)

print("\n===== Similar Players =====")

if result.empty:
    print("❌ No similar players found.")
else:
    print(result.to_string(index=False))