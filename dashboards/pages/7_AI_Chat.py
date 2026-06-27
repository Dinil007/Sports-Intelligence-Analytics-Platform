import sys
from pathlib import Path

# -----------------------------
# Add project root to Python path
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# -----------------------------
# Imports
# -----------------------------
import streamlit as st

from auth.streamlit_auth import is_authenticated

if not is_authenticated():
    st.stop()

from ai.sql_agent import generate_sql
from ai.query_executor import execute_query
from ai.response_generator import explain_results

# -----------------------------
# Page Config handled by central entry point app.py

st.title("🤖 SPORTA VISTA PRO - AI Chat")
st.write("Ask questions about players, teams, scouting, xG, and more.")

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# User input
# -----------------------------
prompt = st.chat_input("Ask SPORTA AI something...")

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # -----------------------------
        # Generate SQL
        # -----------------------------
        sql_query = generate_sql(prompt)

        # -----------------------------
        # Execute SQL
        # -----------------------------
        df = execute_query(sql_query)

        # -----------------------------
        # Generate AI explanation
        # -----------------------------
        explanation = explain_results(
            question=prompt,
            dataframe_text=df.to_string(index=False),
        )

        response_text = (
            "### 📝 Generated SQL\n"
            f"```sql\n{sql_query}\n```\n\n"
            "### 📊 Query Results\n"
            "(See the table below)\n\n"
            "### 🤖 AI Explanation\n"
            f"{explanation}"
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text,
            }
        )

        with st.chat_message("assistant"):
            st.markdown("### 📝 Generated SQL")
            st.code(sql_query, language="sql")

            st.markdown("### 📊 Query Results")
            st.dataframe(df, use_container_width=True)

            st.markdown("### 🤖 AI Explanation")
            st.write(explanation)

    except Exception as e:
        st.error(f"❌ Error: {e}")