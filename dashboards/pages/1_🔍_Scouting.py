import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from database.db_connection import engine

# Page Config handled by central entry point app.py

# ---------------------------------------------------------------------------
# Tier helper
# ---------------------------------------------------------------------------
def sporta_tier(score: float) -> tuple[str, str]:
    """Return (label, colour) for a normalized SPORTA Score."""
    if score >= 90:
        return "Elite", "#10B981"
    elif score >= 80:
        return "Excellent", "#3B82F6"
    elif score >= 70:
        return "Good", "#F59E0B"
    elif score >= 60:
        return "Average", "#8B5CF6"
    else:
        return "Needs Improvement", "#EF4444"


def tier_badge(score: float) -> str:
    label, color = sporta_tier(score)
    return (
        f'<span style="background:{color};color:#fff;padding:2px 10px;'
        f'border-radius:12px;font-size:0.78rem;font-weight:700;">{label}</span>'
    )


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
st.title("🔍 Player Scouting")

min_score = st.slider(
    "Minimum SPORTA Score",
    min_value=40,
    max_value=100,
    value=60,
    step=1,
    help="Score is normalized 0–100. Elite ≥ 90 · Excellent ≥ 80 · Good ≥ 70 · Average ≥ 60"
)

query = f"""
SELECT
    player_name,
    matches_played,
    ROUND(sporta_score::numeric, 2) AS sporta_score,
    goals,
    ROUND(total_xg::numeric, 2)    AS total_xg,
    shots,
    passes,
    dribbles,
    recoveries
FROM vw_scouting
WHERE sporta_score >= {min_score}
ORDER BY sporta_score DESC
LIMIT 100;
"""

df = pd.read_sql(query, engine)

if df.empty:
    st.info("No players found for the selected minimum score.")
else:
    # Add tier column
    df.insert(2, "Tier", df["sporta_score"].apply(lambda s: sporta_tier(s)[0]))

    st.markdown(f"**{len(df)} players** found with SPORTA Score ≥ **{min_score}**")

    # Tier legend
    st.markdown(
        """
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
            <span style="background:#10B981;color:#fff;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">Elite ≥ 90</span>
            <span style="background:#3B82F6;color:#fff;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">Excellent ≥ 80</span>
            <span style="background:#F59E0B;color:#fff;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">Good ≥ 70</span>
            <span style="background:#8B5CF6;color:#fff;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">Average ≥ 60</span>
            <span style="background:#EF4444;color:#fff;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">Needs Improvement &lt; 60</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(df, use_container_width=True, hide_index=True)