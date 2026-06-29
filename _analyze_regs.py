"""Analyze registration sequence numbers in stderr output."""
import sys, re

target_file = sys.argv[1] if len(sys.argv) > 1 else 'd:/stderr_full.txt'

with open(target_file, 'rb') as f:
    data = f.read()

text = data.decode('utf-16-le', errors='replace')

# Count all Reg # values
matches = list(re.finditer(r'Reg # for key: (\d+)', text))
print(f'Total registrations captured: {len(matches)}')

reg_counts = {}
for m in matches:
    v = m.group(1)
    reg_counts[v] = reg_counts.get(v, 0) + 1

print('Reg # distribution:')
for val in sorted(reg_counts.keys()):
    print(f'  Reg # = {val}: {reg_counts[val]}')

# Now specifically analyze the compare_player_Endrick key
print()
print('=== Specific analysis of compare_player_Endrick_Felipe_Moreira_de_Sousa ===')
key = 'compare_player_Endrick_Felipe_Moreira_de_Sousa'
idx = 0
occurrences = []
while True:
    idx = text.find(key, idx)
    if idx < 0:
        break
    # Get the Reg # line nearest to this occurrence
    reg_search = text[max(0, idx-200):idx+50]
    reg_match = re.search(r'Reg # for key: (\d+)', reg_search)
    reg_val = reg_match.group(1) if reg_match else 'NOT FOUND'
    
    # Also get element type
    type_match = re.search(r'Element type:\s+(\S+)', reg_search)
    elem_type = type_match.group(1) if type_match else 'NOT FOUND'
    
    occurrences.append((reg_val, elem_type))
    idx = idx + 1

print(f'Total occurrences: {len(occurrences)}')
for i, (reg, elem) in enumerate(occurrences):
    print(f'  #{i+1}: Reg#={reg}, Element type={elem}')
