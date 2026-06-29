import sys

target_file = sys.argv[1] if len(sys.argv) > 1 else 'd:/stderr_full.txt'
target_key = sys.argv[2] if len(sys.argv) > 2 else 'compare_player_Endrick'

with open(target_file, 'rb') as f:
    data = f.read()

text = data.decode('utf-16-le', errors='replace')

# Find all occurrences
idx = 0
occurrences = []
while True:
    idx = text.find(target_key, idx)
    if idx < 0:
        break
    # Find the start of this registration block (find the previous "-----" divider)
    block_start = text.rfind('---------------', 0, idx)
    if block_start < 0:
        block_start = max(0, idx - 5000)
    # Find the end (next "------")
    block_end = text.find('---------------', idx + 50)
    if block_end < 0:
        block_end = len(text)
    occurrences.append(text[block_start:block_end])
    idx = idx + 1

print(f"Total occurrences of '{target_key}': {len(occurrences)}")
for i, occ in enumerate(occurrences):
    # Extract Reg # and traceback
    lines = occ.split('\n')
    reg_line = [l for l in lines if 'Reg # for key:' in l]
    print(f"\n{'='*80}")
    print(f"OCCURRENCE #{i+1}  |  {reg_line[0].strip() if reg_line else 'NO REG INFO'}")
    print(f"{'='*80}")
    # Print first 5 lines that contain file paths
    file_lines = [l.strip() for l in lines if 'File "' in l]
    for fl in file_lines[:8]:
        print(f"  {fl}")
    print()

# Now also search for Reg #: 1 for this key
reg1_pattern = f"Reg # for key: 1"
idx2 = 0
reg1_occurrences = []
while True:
    idx2 = text.find(reg1_pattern, idx2)
    if idx2 < 0:
        break
    # Find the preceding key
    block_start = max(0, idx2 - 300)
    block_end = min(len(text), idx2 + 50)
    snippet = text[block_start:block_end]
    # Check if the preceding key matches
    if target_key in snippet:
        block_start2 = text.rfind('---------------', 0, idx2)
        if block_start2 < 0:
            block_start2 = max(0, idx2 - 5000)
        block_end2 = text.find('---------------', idx2 + 50)
        if block_end2 < 0:
            block_end2 = len(text)
        reg1_occurrences.append(text[block_start2:block_end2])
    idx2 = idx2 + 1

print(f"\n{'='*80}")
print(f"Reg #: 1 occurrences of '{target_key}': {len(reg1_occurrences)}")
print(f"{'='*80}")
if reg1_occurrences:
    for i, occ in enumerate(reg1_occurrences):
        print(f"\nFIRST REGISTRATION #{i+1}:")
        print(occ[:2000])
else:
    print("NO 'Reg # for key: 1' FOUND IN stderr!")
    print()
    print("Let me search for ALL occurrences of 'Endrick' in stderr...")

# Search for ALL occurrences of 'Endrick'
all_endrick = []
idx3 = 0
while True:
    idx3 = text.find('Endrick', idx3)
    if idx3 < 0:
        break
    block_start3 = text.rfind('---------------', 0, idx3)
    if block_start3 < 0:
        block_start3 = max(0, idx3 - 1000)
    block_end3 = text.find('---------------', idx3 + 50)
    if block_end3 < 0:
        block_end3 = min(len(text), idx3 + 2000)
    all_endrick.append(text[block_start3:block_end3])
    idx3 = idx3 + 1

print(f"\nTotal 'Endrick' occurrences: {len(all_endrick)}")
for i, occ in enumerate(all_endrick):
    lines = occ.split('\n')
    reg_line = [l for l in lines if 'Reg # for key:' in l]
    widget_line = [l for l in lines if 'Widget key:' in l]
    type_line = [l for l in lines if 'Element type:' in l]
    print(f"\n--- Endrick occurrence #{i+1} ---")
    if widget_line: print(f"  {widget_line[0].strip()}")
    if type_line: print(f"  {type_line[0].strip()}")
    if reg_line: print(f"  {reg_line[0].strip()}")
    file_lines = [l.strip() for l in lines if 'File "' in l and 'action_buttons' in l or 'recommendation' in l]
    for fl in file_lines[:4]:
        print(f"  {fl}")

# CRITICAL: Count all Reg # values across ALL keys
print(f"\n{'='*80}")
print("ALL 'Reg # for key:' values analysis")
print(f"{'='*80}")
idx4 = 0
reg_counts = {}  # reg# -> count
while True:
    idx4 = text.find('Reg # for key:', idx4)
    if idx4 < 0:
        break
    line_end = text.find('\n', idx4)
    line = text[idx4:line_end].strip()
    parts = line.split(':')
    if len(parts) >= 2:
        val = parts[-1].strip()
        reg_counts[val] = reg_counts.get(val, 0) + 1
    idx4 = idx4 + 1

for val in sorted(reg_counts.keys()):
    print(f"  Reg # = {val}: count = {reg_counts[val]}")

# Also search for Reg #: 1 near compare_player
print(f"\n{'='*80}")
print("Looking for Reg #: 1 near any compare_player key")
print(f"{'='*80}")
idx5 = 0
for pattern in ['compare_player', 'view_profile', 'export_pdf']:
    pos = 0
    count_1 = 0
    count_2 = 0
    while True:
        pos = text.find(pattern, pos)
        if pos < 0:
            break
        # Find Reg # near this position
        nearby = text[max(0, pos-100):pos+100]
        for val in ['1', '2', '3']:
            if f'Reg # for key: {val}' in nearby:
                if val == '1': count_1 += 1
                elif val == '2': count_2 += 1
        pos = pos + 1
    print(f"  {pattern}: Reg #1 = {count_1}, Reg #2 = {count_2}")
