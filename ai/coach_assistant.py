import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

print("\n🏆 AI Coach Assistant")
print("Type: top players")
print("Type: top scorers")
print("Type: team performance")
print("Type: exit\n")

while True:

    question = input("Coach > ").lower()

    if question == "exit":
        break

    elif question == "top players":

        query = """
        SELECT player_name, sporta_score
        FROM vw_sporta_score
        ORDER BY sporta_score DESC
        LIMIT 10;
        """

        df = pd.read_sql(query, engine)
        print(df)

    elif question == "top scorers":

        query = """
        SELECT player_name, goals
        FROM vw_top_goal_scorers
        LIMIT 10;
        """

        df = pd.read_sql(query, engine)
        print(df)

    elif question == "team performance":

        query = """
        SELECT *
        FROM vw_team_performance
        LIMIT 10;
        """

        df = pd.read_sql(query, engine)
        print(df)

    else:
        print("Unknown command")