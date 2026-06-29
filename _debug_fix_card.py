src_card = "d:/Sports Intelligence & Analytics Platform/dashboards/components/recommendation_card.py"
with open(src_card, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "    # ── Card container ──────────────────────────────────────────────\n    with st.container():",
    '    st.warning(f"CARD START | id={id(player)} | name={name}")\n\n    # ── Card container ──────────────────────────────────────────────\n    with st.container():'
)

content = content.replace(
    "        # DEBUG\\ st.warning(f\"CARD END | id={id(player)} | name={name}\")\n\n        st.divider()",
    '        st.warning(f"CARD END | id={id(player)} | name={name}")\n\n        st.divider()'
)

with open(src_card, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed recommendation_card.py")
