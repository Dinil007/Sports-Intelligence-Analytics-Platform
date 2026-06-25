"""Role-based page registry for SPORTA VISTA PRO navigation."""

from auth.auth_guard import VALID_ROLES, normalize_role

# Each physical page file appears in exactly one registry entry.
PAGE_DEFINITIONS = {
    "home": ("pages/Home.py", "Home", "🏠"),
    "ai_chat": ("pages/7_AI_Chat.py", "AI Chat", "🤖"),
    "ai_coach": ("pages/3_🤖_AI_Coach.py", "AI Coach", "🤖"),
    "xg_analytics": ("pages/2_📈_xG_Analytics.py", "xG Analytics", "📈"),
    "player_comparison": ("pages/8_Player_Comparison.py", "Player Comparison", "⚽"),
    "scouting_reports": ("pages/9_Scouting_Report.py", "Scouting Reports", "📋"),
    "transfer_recs": ("pages/4_🔄_Transfer_Recommendations.py", "Transfer Recommendations", "🔄"),
    "team_analytics": ("pages/Team_Analytics.py", "Team Analytics", "🏟"),
    "injury_risk": ("pages/5_🏥_Injury_Risk.py", "Injury Risk", "🏥"),
    "admin_panel": ("pages/Admin.py", "Admin Panel", "⚙️"),
    "scouting": ("pages/1_🔍_Scouting.py", "Scouting", "🔍"),
    "ai_player_recs": ("pages/10_AI_Player_Recommendations.py", "AI Player Recommendations", "🔄"),
}

ROLE_PAGE_KEYS = {
    "admin": [
        "home",
        "ai_chat",
        "ai_coach",
        "xg_analytics",
        "player_comparison",
        "scouting_reports",
        "transfer_recs",
        "team_analytics",
        "injury_risk",
        "admin_panel",
    ],
    "scout": [
        "home",
        "scouting",
        "player_comparison",
        "scouting_reports",
        "transfer_recs",
        "ai_player_recs",
    ],
    "coach": [
        "home",
        "ai_coach",
        "ai_chat",
        "team_analytics",
        "injury_risk",
    ],
    "analyst": [
        "home",
        "xg_analytics",
        "team_analytics",
        "scouting_reports",
    ],
}


def get_page_paths_for_role(role: str) -> list[str]:
    """Return ordered page file paths allowed for a role."""
    normalized = normalize_role(role)
    keys = ROLE_PAGE_KEYS.get(normalized, [])
    return [PAGE_DEFINITIONS[key][0] for key in keys]


def is_valid_role(role: str) -> bool:
    normalized = normalize_role(role)
    return normalized in VALID_ROLES and normalized in ROLE_PAGE_KEYS
