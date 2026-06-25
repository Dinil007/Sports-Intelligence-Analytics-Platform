from ai.sql_agent import generate_sql
from ai.query_executor import execute_query
from ai.response_generator import explain_results

question = "Show the top 10 players by SPORTA Score"

# Generate SQL
sql = generate_sql(question)
print("\nGenerated SQL:")
print(sql)

# Execute SQL
df = execute_query(sql)
print("\nRaw Results:")
print(df)

# Explain Results
summary = explain_results(
    question=question,
    dataframe_text=df.to_string(index=False)
)

print("\nAI Summary:")
print(summary)