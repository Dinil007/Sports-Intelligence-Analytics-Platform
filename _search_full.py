import os
import re

root = "d:/Sports Intelligence & Analytics Platform"
skip_dirs = {".git", "venv"}  # keep venv to be safe, but we'll search all py files

# Patterns we are looking for
st_button_pattern = re.compile(r'st\.button\(')
import_action_buttons_pattern = re.compile(r'^(?:from\s+dashboards\.components\.action_buttons\s+import|import\s+dashboards\.components\.action_buttons)')
render_recommendation_card_pattern = re.compile(r'render_recommendation_card\(')

button_calls = []  # list of dicts
imports = []
render_calls = []

for dirpath, dirnames, filenames in os.walk(root):
    # We won't prune dirs so we search everything, but we can still skip .git
    dirnames[:] = [d for d in dirnames if d != ".git"]
    for fname in filenames:
        if not fname.endswith(".py"):
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue

        # Search for st.button( and capture multi-line call
        for i, line in enumerate(lines, 1):
            if st_button_pattern.search(line):
                # Collect lines until we find the closing )
                start = i - 1
                call_lines = [line.rstrip("\n")]
                j = start
                balance = call_lines[0].count('(') - call_lines[0].count(')')
                while balance > 0 and j + 1 < len(lines):
                    j += 1
                    call_lines.append(lines[j].rstrip("\n"))
                    balance = call_lines[-1].count('(') - call_lines[-1].count(')')
                full_call = "\n".join(call_lines)
                # Extract key= argument
                key_match = re.search(r'key\s*=\s*("[^"]*"|\'[^\']*\')', full_call)
                key_arg = key_match.group(1) if key_match else "None"
                button_calls.append({
                    "file": fpath,
                    "line": i,
                    "call": full_call,
                    "key": key_arg,
                })

            # Search for imports
            if import_action_buttons_pattern.search(line):
                imports.append((fpath, i, line.rstrip()))

            # Search for render_recommendation_card(
            if render_recommendation_card_pattern.search(line):
                render_calls.append((fpath, i, line.rstrip()))

# Now print results
print("=== ST.BUTTON CALLS ===")
for b in button_calls:
    print(f"FILE: {b['file']}")
    print(f"LINE: {b['line']}")
    print(f"CALL:\n{b['call']}")
    print(f"KEY: {b['key']}")
    print("-" * 60)

print("\n=== IMPORTS OF dashboards.components.action_buttons ===")
for fpath, i, line in imports:
    print(f"{fpath}:{i}: {line}")

print("\n=== render_recommendation_card CALLS ===")
for fpath, i, line in render_calls:
    print(f"{fpath}:{i}: {line}")

print("\n=== SUMMARY ===")
print(f"Total st.button calls: {len(button_calls)}")
print(f"Total imports: {len(imports)}")
print(f"Total render_recommendation_card calls: {len(render_calls)}")

# Question 1: any st.button key that could evaluate to compare_player_Endrick_Felipe_Moreira_de_Sousa?
# This would be a dynamic key built from player_name. The pattern in action_buttons.py is:
# action_key = f"{label.lower().replace(' ', '_')}_{safe_key}"
# where safe_key = player_name.replace(" ", "_").replace(".", "")
# So for Compare Player label and player_name "Endrick Felipe Moreira de Sousa", the key is:
# compare_player_Endrick_Felipe_Moreira_de_Sousa
# We need to see if any other st.button uses a similar dynamic pattern.
# We'll flag any st.button where the key contains "compare_player_" or is dynamic (evaluates from player_name).
# For static keys, we can just match exactly.

target_key = 'compare_player_Endrick_Felipe_Moreira_de_Sousa'
print(f"\nQuestion 1: Search for key that can evaluate to {target_key}")
for b in button_calls:
    if b['key'] != "None":
        if b['key'] == target_key:
            print(f"  EXACT MATCH: {b['file']}:{b['line']}")
        elif "compare_player_" in b['key']:
            print(f"  DYNAMIC/POSSIBLE: {b['file']}:{b['line']} -> {b['key']}")
    else:
        # Check if the call uses a dynamic key expression (e.g., key=action_key, key=f"...")
        if re.search(r'key\s*=\s*(action_key|f["\'])', b['call']):
            print(f"  DYNAMIC KEY: {b['file']}:{b['line']} -> {b['call'].splitlines()[-1]}")
