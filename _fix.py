from pathlib import Path
p = Path(r'dashboards\components\recommendation_card.py')
lines = p.read_text(encoding='utf-8').splitlines()
start = None
end = None
for i, line in enumerate(lines):
    if '# Action buttons' in line and start is None:
        start = i
    if start is not None and 'st.toast(' in line:
        end = i
        break
if start is None or end is None:
    raise SystemExit('not found')
new = [
    '        # Action buttons ------------------',
    '        cols = st.columns(3)',
    '',
    '        unique_id = player.get("player_id")',
    '        if unique_id is None:',
    '            unique_id = f"idx_{index}"',
    '',
    '        actions = [',
    '            ("Compare Player", f"compare_{unique_id}"),',
    '            ("View Profile", f"profile_{unique_id}"),',
    '            ("Export PDF", f"pdf_{unique_id}")',
    '        ]',
    '',
    '        for col, (label, key) in zip(cols, actions):',
    '            with col:',
    '                if st.button(label, key=key, use_container_width=True):',
    '                    if label == "Compare Player":',
    '                        st.session_state["compare_player"] = player["player_name"]',
]
lines[start:end+1] = new
p.write_text('\n'.join(lines), encoding='utf-8', newline='\r\n')
print('CARD OK')
