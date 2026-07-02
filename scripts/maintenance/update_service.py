path = 'd:/Sports Intelligence & Analytics Platform/services/recommendation_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_imports = '''from __future__ import annotations

from typing import Any

from database.recommendation_repository import get_candidate_players, get_player_vector
from ml.recommendation_engine import (
    FEATURE_COLUMNS,
    calculate_similarity,
    prepare_feature_matrix,
    rank_players,
)'''

new_imports = '''from __future__ import annotations

import numpy as np
from typing import Any

from database.recommendation_repository import get_candidate_players, get_player_vector
from ml.recommendation_engine import (
    FEATURE_COLUMNS,
    calculate_similarity,
    prepare_feature_matrix,
    rank_players,
)'''

old_return = '''        results.append({
            "player_name": r.player_name,
            "team": r.team_name or "N/A",
            "competition": "N/A",
            "sporta_score": r.sporta_score,
            "similarity": r.similarity,
            "goals": r.goals,
            "total_xg": r.total_xg,
            "passes": r.passes,
            "dribbles": r.dribbles,
            "carries": r.carries,
            "recoveries": r.recoveries,
            "pressures": r.pressures,
        })'''

new_return = '''        tier = _sporta_tier(r.sporta_score)
        results.append({
            "player_name": r.player_name,
            "club": r.team_name or "N/A",
            "nationality": "N/A",
            "position": "N/A",
            "age": None,
            "minutes_played": None,
            "sporta_score": r.sporta_score,
            "sporta_tier": tier,
            "similarity_pct": r.similarity,
            "badge_color": _badge_color(tier),
            "goals": r.goals,
            "assists": 0,
            "total_xg": r.total_xg,
            "pass_accuracy": None,
            "passes": r.passes,
            "dribbles": r.dribbles,
            "carries": r.carries,
            "recoveries": r.recoveries,
            "pressures": r.pressures,
            "progressive_passes": None,
            "preferred_foot": "N/A",
        })'''

old_func_end = '''    # Import numpy locally to avoid hard dependency at module level for non-ML paths
import numpy as np  # noqa: E402'''

new_func_end = '''    # Import numpy locally to avoid hard dependency at module level for non-ML paths
import numpy as np  # noqa: E402


def _sporta_tier(score: float) -> str:
    """Map SPORTA score to a tier label."""
    if score >= 85:
        return "Elite"
    if score >= 70:
        return "High"
    if score >= 55:
        return "Medium"
    return "Low"


def _badge_color(tier: str) -> str:
    """Map tier to a color class for UI rendering."""
    mapping = {
        "Elite": "#ef4444",
        "High": "#f59e0b",
        "Medium": "#3b82f6",
        "Low": "#10b981",
    }
    return mapping.get(tier, "#64748b")'''

for old, new in [(old_imports, new_imports), (old_return, new_return), (old_func_end, new_func_end)]:
    if old not in content:
        print(f'NOT FOUND: {old[:80]}')
    else:
        content = content.replace(old, new)
        print('REPLACED')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Service updated')
