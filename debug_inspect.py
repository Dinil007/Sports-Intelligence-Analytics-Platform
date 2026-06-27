import sys
txt = open('d:/Sports Intelligence & Analytics Platform/dashboards/pages/4_🔄_Transfer_Recommendations.py', 'r', encoding='utf-8').read()
# Show lines around the import area
lines = txt.split('\n')
for i, line in enumerate(lines, 1):
    if 'recommendation' in line or 'card_styles' in line or 'dashboards' in line or i in range(1, 30):
        print(f'{i:3d}: {line}')
