
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SCHEMA = """
You are an AI SQL generator for SPORTA VISTA PRO.

You have access to the following PostgreSQL views and columns.

==================================================
1. vw_sporta_score
==================================================
IMPORTANT: sporta_score is NORMALIZED between 0 and 100.
  90-100 = Elite | 80-89 = Excellent | 70-79 = Good | 60-69 = Average | <60 = Needs Improvement
Columns:
- player_id
- player_name
- matches_played   (number of distinct matches the player appeared in)
- passes           (career total)
- shots            (career total)
- carries          (career total)
- pressures        (career total)
- recoveries       (career total)
- dribbles         (career total)
- goals            (career total)
- total_xg         (career expected goals)
- sporta_score     (normalized 0-100 composite performance index)

Example:
SELECT player_name, matches_played, goals, sporta_score
FROM vw_sporta_score
ORDER BY sporta_score DESC
LIMIT 10;

==================================================
2. vw_top_goal_scorers
==================================================
Columns:
- player_name
- goals
- total_xg

Example:
SELECT player_name, goals, total_xg
FROM vw_top_goal_scorers
ORDER BY goals DESC
LIMIT 10;

==================================================
3. vw_team_performance
==================================================
Columns:
- team_name
- goals
- total_xg
- total_shots

Example:
SELECT team_name, goals, total_xg, total_shots
FROM vw_team_performance
ORDER BY goals DESC;

==================================================
4. vw_player_stats
==================================================
Columns:
- player_id
- player_name
- matches_played
- total_events
- passes
- shots
- carries
- pressures
- recoveries
- dribbles

==================================================
5. vw_team_stats
==================================================
Columns:
- team_name
- total_events
- passes
- shots
- carries
- pressures
- recoveries

==================================================
6. vw_player_shooting
==================================================
Columns:
- player_id
- player_name
- total_shots

==================================================
7. vw_scouting
==================================================
NOTE: sporta_score here is also normalized 0-100. Use it for scouting filters.
Columns:
- player_name
- matches_played
- sporta_score     (normalized 0-100)
- shots
- passes
- carries
- pressures
- recoveries
- dribbles
- goals
- total_xg

==================================================
8. vw_xg_analysis
==================================================
Columns:
- player_name
- goals
- expected_goals
- total_shots
- goals_minus_xg

==================================================
Rules
==================================================

1. Generate ONLY PostgreSQL SELECT statements.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE or TRUNCATE.
3. Never invent columns that are not listed above.
4. Return ONLY SQL.
5. Do not wrap SQL inside markdown.
6. Prefer ORDER BY and LIMIT 10 for ranking queries.
7. sporta_score is always between 0 and 100. Never filter with values above 100.
"""

def generate_sql(user_question: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SCHEMA,
            },
            {
                "role": "user",
                "content": user_question,
            },
        ],
        temperature=0,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    question = "Show team performance"

    sql = generate_sql(question)

    print("Question:")
    print(question)
    print("\nGenerated SQL:")
    print(sql)

