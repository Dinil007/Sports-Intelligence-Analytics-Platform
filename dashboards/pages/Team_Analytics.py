import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_connection import engine

st.title("🏟️ Team Performance Analytics")
st.markdown("Analyze overall team standings, goal production, and xG efficiency across the league.")

st.divider()

try:
    # Fetch team performance data
    team_df = pd.read_sql("""
        SELECT 
            team_name, 
            goals, 
            total_xg, 
            total_shots,
            ROUND((goals - total_xg)::numeric, 2) as xg_difference
        FROM vw_team_performance
        ORDER BY goals DESC;
    """, engine)

    if team_df.empty:
        st.warning("No team performance data found.")
    else:
        # Display KPIs
        total_teams = len(team_df)
        total_goals = team_df["goals"].sum()
        avg_xg = team_df["total_xg"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Teams", total_teams)
        col2.metric("Total Goals Scored", int(total_goals))
        col3.metric("Avg Expected Goals (xG)", round(float(avg_xg), 2))

        st.write("")

        # Display dataframe
        st.subheader("📊 Team Leaderboard")
        st.dataframe(
            team_df,
            use_container_width=True,
            hide_index=True
        )

        st.write("")

        # Charts Section
        st.subheader("📈 Visual Performance Metrics")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig_goals = px.bar(
                team_df,
                x="team_name",
                y="goals",
                title="Goals Scored by Team",
                labels={"team_name": "Team", "goals": "Goals"},
                color="goals",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_goals, use_container_width=True)

        with chart_col2:
            # Sort by xG difference to show overperforming vs underperforming
            df_sorted = team_df.sort_values(by="xg_difference", ascending=False)
            fig_xg = px.bar(
                df_sorted,
                x="team_name",
                y="xg_difference",
                title="Goal Overperformance vs. Underperformance (Goals - xG)",
                labels={"team_name": "Team", "xg_difference": "Goals - xG Difference"},
                color="xg_difference",
                color_continuous_scale="RdBu",
                color_continuous_midpoint=0
            )
            st.plotly_chart(fig_xg, use_container_width=True)

except Exception as e:
    st.error(f"Error loading team analytics: {e}")
