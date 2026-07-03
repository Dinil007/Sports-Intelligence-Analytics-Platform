"""Role-based page registry for SPORTA VISTA PRO navigation."""

from pathlib import Path

from auth.auth_guard import VALID_ROLES, normalize_role

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Each physical page file appears in exactly one registry entry.
# Paths are absolute, built from this file's location.
PAGE_DEFINITIONS = {
    "home": (PROJECT_ROOT / "dashboards" / "pages" / "Home.py", "Home", "🏠"),
    "ai_chat": (PROJECT_ROOT / "dashboards" / "pages" / "7_AI_Chat.py", "AI Chat", "🤖"),
    "ai_coach": (PROJECT_ROOT / "dashboards" / "pages" / "3_🤖_AI_Coach.py", "AI Coach", "🤖"),
    "xg_analytics": (PROJECT_ROOT / "dashboards" / "pages" / "2_📈_xG_Analytics.py", "xG Analytics", "📈"),
    "player_comparison": (PROJECT_ROOT / "dashboards" / "pages" / "8_Player_Comparison.py", "Player Comparison", "⚽"),
    "scouting_reports": (PROJECT_ROOT / "dashboards" / "pages" / "9_Scouting_Report.py", "Scouting Reports", "📋"),
    "transfer_recs": (PROJECT_ROOT / "dashboards" / "pages" / "4_🔄_Transfer_Recommendations.py", "AI Transfer Recommendations", "🔄"),
    "transfer_advisor": (PROJECT_ROOT / "dashboards" / "pages" / "6_🔄_Transfer_Advisor.py", "Transfer Advisor", "🔄"),
    "team_analytics": (PROJECT_ROOT / "dashboards" / "pages" / "Team_Analytics.py", "Team Analytics", "🏟"),
    "injury_risk": (PROJECT_ROOT / "dashboards" / "pages" / "5_🏥_Injury_Risk.py", "Injury Risk", "🏥"),
    "admin_panel": (PROJECT_ROOT / "dashboards" / "pages" / "Admin.py", "Admin Panel", "⚙️"),
    "scouting": (PROJECT_ROOT / "dashboards" / "pages" / "1_🔍_Scouting.py", "Scouting", "🔍"),
    "match_intelligence": (PROJECT_ROOT / "dashboards" / "pages" / "11_⚽_Match_Intelligence.py", "Match Intelligence", "⚽"),
    "scouting_recruitment": (PROJECT_ROOT / "dashboards" / "pages" / "12_🔍_Scouting_Recruitment.py", "Scouting & Recruitment", "🔍"),
    "transfer_intelligence": (PROJECT_ROOT / "dashboards" / "pages" / "13_💰_Transfer_Intelligence.py", "Transfer Intelligence", "💰"),
    "athlete_monitoring": (PROJECT_ROOT / "dashboards" / "pages" / "14_🏃_Athlete_Monitoring.py", "Athlete Monitoring", "🏃"),
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
        "transfer_advisor",
        "team_analytics",
        "injury_risk",
        "admin_panel",
        "match_intelligence",
        "scouting_recruitment",
        "transfer_intelligence",
        "athlete_monitoring",
    ],
    "scout": [
        "home",
        "scouting",
        "scouting_recruitment",
        "transfer_intelligence",
        "athlete_monitoring",
        "player_comparison",
        "scouting_reports",
        "transfer_recs",
        "transfer_advisor",
    ],
    "coach": [
        "home",
        "ai_coach",
        "ai_chat",
        "team_analytics",
        "athlete_monitoring",
        "injury_risk",
    ],
    "analyst": [
        "home",
        "xg_analytics",
        "team_analytics",
        "scouting_reports",
        "scouting_recruitment",
        "transfer_intelligence",
        "athlete_monitoring",
    ],
}


def get_page_paths_for_role(role: str) -> list[str]:
    """Return ordered page file paths allowed for a role."""
    normalized = normalize_role(role)
    keys = ROLE_PAGE_KEYS.get(normalized, [])
    return [str(PAGE_DEFINITIONS[key][0]) for key in keys]


def is_valid_role(role: str) -> bool:
    normalized = normalize_role(role)
    return normalized in VALID_ROLES and normalized in ROLE_PAGE_KEYS
