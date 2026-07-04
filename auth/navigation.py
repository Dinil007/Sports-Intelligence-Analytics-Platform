"""Role-based page registry for SPORTA VISTA PRO navigation.

Architecture:
  PAGE_DEFINITIONS  — single source of truth: key → (path, title, icon)
  ROLE_PAGE_KEYS    — flat ordered key list per role (backward compat / tests)
  ROLE_PAGE_GROUPS  — ordered section dict per role used by st.navigation()
                      Maps  SectionHeader → [page keys]
                      This is the permanent fix for sidebar overflow: grouped
                      navigation scales to any number of future phases.
"""

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
    "executive_bi": (PROJECT_ROOT / "dashboards" / "pages" / "16_📊_Executive_Business_Intelligence.py", "Executive Business Intelligence", "📊"),
    "mlops_platform": (PROJECT_ROOT / "dashboards" / "pages" / "17_🤖_MLOps_Platform.py", "MLOps Platform", "🤖"),
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
        "executive_bi",
        "mlops_platform",
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
        "executive_bi",
        "mlops_platform",
    ],
}


# ── Grouped navigation ────────────────────────────────────────────────────────
# Each role maps to an ordered dict of  { "Section Label": [page_key, ...] }
# st.navigation() accepts this Mapping directly (Streamlit 1.42+).
# Adding a new phase = add one new entry here; the sidebar never overflows.

ROLE_PAGE_GROUPS: dict[str, dict[str, list[str]]] = {
    "admin": {
        "Home": ["home"],
        "AI Assistants": ["ai_chat", "ai_coach"],
        "Analytics": ["xg_analytics", "team_analytics", "match_intelligence"],
        "Players": ["player_comparison", "injury_risk"],
        "Scouting": ["scouting_reports", "scouting_recruitment"],
        "Transfers": ["transfer_recs", "transfer_advisor", "transfer_intelligence"],
        "Monitoring": ["athlete_monitoring"],
        "Management": ["executive_bi", "admin_panel"],
        "Platform": ["mlops_platform"],
    },
    "scout": {
        "Home": ["home"],
        "Scouting": ["scouting", "scouting_recruitment", "scouting_reports"],
        "Players": ["player_comparison", "athlete_monitoring"],
        "Transfers": ["transfer_recs", "transfer_advisor", "transfer_intelligence"],
    },
    "coach": {
        "Home": ["home"],
        "AI Assistants": ["ai_coach", "ai_chat"],
        "Team": ["team_analytics"],
        "Monitoring": ["athlete_monitoring", "injury_risk"],
    },
    "analyst": {
        "Home": ["home"],
        "Analytics": ["xg_analytics", "team_analytics"],
        "Scouting": ["scouting_reports", "scouting_recruitment"],
        "Transfers": ["transfer_intelligence"],
        "Monitoring": ["athlete_monitoring"],
        "Management": ["executive_bi"],
        "Platform": ["mlops_platform"],
    },
}


def get_page_paths_for_role(role: str) -> list[str]:
    """Return ordered page file paths allowed for a role (flat, for tests)."""
    normalized = normalize_role(role)
    keys = ROLE_PAGE_KEYS.get(normalized, [])
    return [str(PAGE_DEFINITIONS[key][0]) for key in keys]


def is_valid_role(role: str) -> bool:
    normalized = normalize_role(role)
    return normalized in VALID_ROLES and normalized in ROLE_PAGE_KEYS
