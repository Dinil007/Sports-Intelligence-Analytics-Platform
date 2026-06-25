from ai.sql_agent import generate_sql
from ai.query_executor import execute_query

question = "Show the top 10 players by SPORTA Score"

# Generate SQL
sql = generate_sql(question)

print("Generated SQL:")
print(sql)

print("\nResults:")
df = execute_query(sql)
print(df)