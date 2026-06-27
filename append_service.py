path = 'd:/Sports Intelligence & Analytics Platform/services/recommendation_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

helpers = """


def _sporta_tier(score: float) -> str:
    \"\"\"Map SPORTA score to a tier label.\"\"\"
    if score >= 85:
        return "Elite"
    if score >= 70:
        return "High"
    if score >= 55:
        return "Medium"
    return "Low"


def _badge_color(tier: str) -> str:
    \"\"\"Map tier to a color class for UI rendering.\"\"\"
    mapping = {
        "Elite": "#ef4444",
        "High": "#f59e0b",
        "Medium": "#3b82f6",
        "Low": "#10b981",
    }
    return mapping.get(tier, "#64748b")
"""

# Check if already appended
if "_sporta_tier" not in content:
    content += helpers
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Helpers appended')
else:
    print('Helpers already exist')
