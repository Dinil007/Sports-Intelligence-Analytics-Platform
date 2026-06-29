import subprocess
p = subprocess.run(
    ['git', 'show', 'HEAD:dashboards/components/recommendation_comparison.py'],
    capture_output=True, text=True,
    cwd=r'd:\Sports Intelligence & Analytics Platform'
)
print(p.stdout[:5000])
if p.stderr:
    print('STDERR:', p.stderr[:500])
