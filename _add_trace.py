src = "d:/Sports Intelligence & Analytics Platform/dashboards/components/action_buttons.py"
with open(src, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
    "import streamlit as st",
    "import traceback\n\nimport streamlit as st"
)

c = c.replace(
    '            st.write(f"CREATING BUTTON: {action_key}")\n            if st.button(',
    '            st.code("".join(traceback.format_stack(limit=12)), language="text")\n            st.write("PLAYER:", player_name)\n            st.write("KEY:", action_key)\n            if st.button('
)

with open(src, "w", encoding="utf-8") as f:
    f.write(c)

print("Done")
