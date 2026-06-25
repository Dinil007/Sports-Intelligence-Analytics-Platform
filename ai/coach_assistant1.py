import traceback

from ai.sql_agent import generate_sql
from ai.query_executor import execute_query
from ai.response_generator import explain_results


print("\n" + "=" * 60)
print("🏆 SPORTA VISTA PRO - AI COACH")
print("=" * 60)

print("\nYou can ask questions like:")
print("• Show the top 10 players by SPORTA Score")
print("• Who are the top scorers?")
print("• Show team performance")
print("• List players with highest SPORTA Score")
print("• Show top goal scorers")
print("• exit\n")

while True:
    try:
        # ----------------------------
        # Get user question
        # ----------------------------
        question = input("Coach > ").strip()

        if question.lower() == "exit":
            print("\n👋 Exiting SPORTA AI Coach...")
            break

        # ----------------------------
        # Step 1: Generate SQL
        # ----------------------------
        sql_query = generate_sql(question)

        print("\n📝 Generated SQL:")
        print(sql_query)

        # ----------------------------
        # Step 2: Basic safety check
        # ----------------------------
        sql_lower = sql_query.strip().lower()

        if not (
            sql_lower.startswith("select")
            or sql_lower.startswith("with")
        ):
            print("\n❌ Unsafe SQL detected. Query blocked.")
            continue

        # ----------------------------
        # Step 3: Execute SQL
        # ----------------------------
        df = execute_query(sql_query)

        if df.empty:
            print("\n⚠️ No results found.")
            continue

        # ----------------------------
        # Step 4: Display raw results
        # ----------------------------
        print("\n📊 Database Results:")
        print(df)

        # ----------------------------
        # Step 5: AI Explanation
        # ----------------------------
        summary = explain_results(
            question=question,
            dataframe_text=df.to_string(index=False)
        )

        print("\n🤖 SPORTA AI Coach:")
        print(summary)

    except Exception as e:
        print("\n❌ Error occurred:")
        print(e)

        # Uncomment while debugging
        traceback.print_exc()