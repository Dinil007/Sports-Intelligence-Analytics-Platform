import streamlit as st
import pandas as pd
from sqlalchemy import text
from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from database.db_connection import engine

# Page Config handled by central entry point app.py

st.title("🔄 Transfer Recommendation Engine")
st.markdown("Find players with high SPORTA Scores and strong attacking output.")

# ---------------------------------------------------------------------------
# Tier helper
# ---------------------------------------------------------------------------
def sporta_tier(score: float) -> tuple[str, str]:
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


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    min_sporta = st.slider(
        "Minimum SPORTA Score",
        min_value=40,
        max_value=100,
        value=70,
        step=1,
        help="Normalized 0–100. Elite ≥ 90 · Excellent ≥ 80 · Good ≥ 70"
    )

with col2:
    min_goals = st.slider(
        "Minimum Goals",
        min_value=0,
        max_value=50,
        value=3,
        step=1,
    )

# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------
query = text("""
SELECT
    player_name,
    matches_played,
    ROUND(sporta_score::numeric, 2) AS sporta_score,
    goals,
    ROUND(total_xg::numeric, 2)    AS total_xg,
    shots,
    passes,
    carries,
    dribbles,
    recoveries
FROM vw_scouting
WHERE sporta_score >= :min_sporta
  AND goals        >= :min_goals
ORDER BY sporta_score DESC, goals DESC
LIMIT 100;
""")

df = pd.read_sql(
    query,
    engine,
    params={"min_sporta": min_sporta, "min_goals": min_goals},
)

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
st.subheader("🎯 Recommended Players")

if df.empty:
    st.info("No players match the current filters. Try lowering the sliders.")
else:
    df.insert(2, "Tier", df["sporta_score"].apply(lambda s: sporta_tier(s)[0]))
    st.markdown(f"**{len(df)} players** found.")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ---------------------------------------------------------------------------
    # Chart — SPORTA Score bar chart (capped at 30 players for readability)
    # ---------------------------------------------------------------------------
    st.subheader("📊 SPORTA Score Comparison")
    chart_df = (
        df.head(30)[["player_name", "sporta_score"]]
        .set_index("player_name")
    )
    st.bar_chart(chart_df)

st.info(
    f"Showing players with SPORTA Score ≥ {min_sporta} "
    f"and Goals ≥ {min_goals}."
)