from ai.sql_agent import generate_sql

question = "Show the top 10 players by SPORTA Score"

sql = generate_sql(question)

print("Generated SQL:")
print(sql)