import sys
from pathlib import Path
from datetime import datetime

# -----------------------------------
# Add project root to Python path
# -----------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# -----------------------------------
# Imports
# -----------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px

from database.db_connection import engine

# Page Config handled by central entry point app.py

# -----------------------------------
# Header & Welcome Section
# -----------------------------------
username = st.session_state.get("username", "User").capitalize()
user_role = st.session_state.get("role", "").upper()
current_time = datetime.now().strftime("%A, %b %d, %Y | %H:%M")

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1.5rem;
    ">
        <h1 style="margin: 0; color: #38bdf8; font-size: 2.2rem; font-weight: 800;">🏆 SPORTA VISTA PRO</h1>
        <p style="margin: 0.5rem 0 0 0; color: #94a3b8; font-size: 1.1rem;">
            Welcome back, <strong style="color: #f8fafc;">{username}</strong> &nbsp;|&nbsp; Role: <span style="color: #38bdf8; font-weight: 600;">{user_role}</span>
        </p>
        <p style="margin: 0.25rem 0 0 0; color: #64748b; font-size: 0.85rem;">
            {current_time}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# KPI Cards
# -----------------------------------
try:
    total_players = pd.read_sql("""
        SELECT COUNT(DISTINCT player_name) AS total_players
        FROM vw_scouting;
    """, engine).iloc[0]["total_players"]

    total_goals = pd.read_sql("""
        SELECT COALESCE(SUM(goals),0) AS total_goals
        FROM vw_top_goal_scorers;
    """, engine).iloc[0]["total_goals"]

    avg_sporta = pd.read_sql("""
        SELECT AVG(sporta_score) AS avg_score
        FROM vw_sporta_score;
    """, engine).iloc[0]["avg_score"]

    max_sporta = pd.read_sql("""
        SELECT MAX(sporta_score) AS max_score
        FROM vw_sporta_score;
    """, engine).iloc[0]["max_score"]

    c1, c2, c3, c4 = st.columns(4)

    # Display clean metric cards
    with c1:
        st.markdown('<div style="background-color: #1e293b; padding: 1rem; border-radius: 8px; border: 1px solid #334155;">', unsafe_allow_html=True)
        st.metric("👥 Total Players", int(total_players))
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="background-color: #1e293b; padding: 1rem; border-radius: 8px; border: 1px solid #334155;">', unsafe_allow_html=True)
        st.metric("⚽ Total Goals", int(total_goals))
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div style="background-color: #1e293b; padding: 1rem; border-radius: 8px; border: 1px solid #334155;">', unsafe_allow_html=True)
        st.metric("📈 Average SPORTA Score", round(float(avg_sporta), 2))
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div style="background-color: #1e293b; padding: 1rem; border-radius: 8px; border: 1px solid #334155;">', unsafe_allow_html=True)
        st.metric("🏆 Highest SPORTA Score", round(float(max_sporta), 2))
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"KPI Error: {e}")

st.write("")

# -----------------------------------
# Quick Actions Section (role-aware)
# -----------------------------------
st.subheader("⚡ Quick Actions")

ROLE_QUICK_ACTIONS = {
    "admin": [
        ("🤖 AI Chat", "pages/7_AI_Chat.py"),
        ("⚽ Player Comparison", "pages/8_Player_Comparison.py"),
        ("📋 Scouting Reports", "pages/9_Scouting_Report.py"),
        ("🔄 Transfer Recommendations", "pages/4_🔄_Transfer_Recommendations.py"),
    ],
    "scout": [
        ("🔍 Scouting", "pages/1_🔍_Scouting.py"),
        ("⚽ Player Comparison", "pages/8_Player_Comparison.py"),
        ("📋 Scouting Reports", "pages/9_Scouting_Report.py"),
        ("🔄 Transfer Recommendations", "pages/4_🔄_Transfer_Recommendations.py"),
    ],
    "coach": [
        ("🤖 AI Coach", "pages/3_🤖_AI_Coach.py"),
        ("🤖 AI Chat", "pages/7_AI_Chat.py"),
        ("🏟 Team Analytics", "pages/Team_Analytics.py"),
        ("🏥 Injury Risk", "pages/5_🏥_Injury_Risk.py"),
    ],
    "analyst": [
        ("📈 xG Analytics", "pages/2_📈_xG_Analytics.py"),
        ("🏟 Team Analytics", "pages/Team_Analytics.py"),
        ("📋 Scouting Reports", "pages/9_Scouting_Report.py"),
    ],
}

quick_actions = ROLE_QUICK_ACTIONS.get(st.session_state.get("role"), [])


def safe_switch(page_path):
    try:
        st.switch_page(page_path)
    except Exception:
        st.error("🛑 Access Denied: You do not have permission to view this page.")

if quick_actions:
    cols = st.columns(len(quick_actions))
    for col, (label, page_path) in zip(cols, quick_actions):
        with col:
            if st.button(label, use_container_width=True, type="secondary"):
                safe_switch(page_path)

st.write("")

# -----------------------------------
# Recent Insights Section
# -----------------------------------
st.subheader("💡 Recent Insights")
try:
    top_player_df = pd.read_sql("SELECT player_name, sporta_score FROM vw_sporta_score ORDER BY sporta_score DESC LIMIT 1;", engine)
    top_player = top_player_df.iloc[0]["player_name"] if not top_player_df.empty else "N/A"
    top_score = top_player_df.iloc[0]["sporta_score"] if not top_player_df.empty else 0.0

    top_scorer_df = pd.read_sql("SELECT player_name, goals FROM vw_top_goal_scorers ORDER BY goals DESC LIMIT 1;", engine)
    top_scorer = top_scorer_df.iloc[0]["player_name"] if not top_scorer_df.empty else "N/A"
    top_goals = top_scorer_df.iloc[0]["goals"] if not top_scorer_df.empty else 0

    top_team_df = pd.read_sql("SELECT team_name, goals FROM vw_team_performance ORDER BY goals DESC LIMIT 1;", engine)
    top_team = top_team_df.iloc[0]["team_name"] if not top_team_df.empty else "N/A"
    top_team_goals = top_team_df.iloc[0]["goals"] if not top_team_df.empty else 0

    ai_summary = f"🤖 **SPORTA Insights Bot**: *{top_player}* is currently our highest-performing athlete with a SPORTA score of **{top_score:.1f}**. The golden boot frontrunner is *{top_scorer}* scoring **{int(top_goals)}** goals. Team performance stats highlight *{top_team}* leading overall offensive stats with **{int(top_team_goals)}** team goals."

    st.markdown(
        f"""
        <div style="
            background-color: #1e293b;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 5px solid #38bdf8;
            border-top: 1px solid #334155;
            border-right: 1px solid #334155;
            border-bottom: 1px solid #334155;
            margin-bottom: 1.5rem;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <div>🌟 <strong>Top Player:</strong> {top_player} ({top_score:.1f})</div>
                <div>🔥 <strong>Top Goal Scorer:</strong> {top_scorer} ({int(top_goals)} goals)</div>
                <div>🏟️ <strong>Highest Goal Team:</strong> {top_team} ({int(top_team_goals)} goals)</div>
            </div>
            <p style="margin: 0; color: #e2e8f0; font-size: 0.95rem; font-style: italic;">
                {ai_summary}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
except Exception as e:
    st.error(f"Insights Section Error: {e}")

# -----------------------------------
# Two-Column Responsive Chart Layout
# -----------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    try:
        df_players = pd.read_sql("""
            SELECT player_name, sporta_score
            FROM vw_sporta_score
            ORDER BY sporta_score DESC
            LIMIT 10;
        """, engine)

        fig = px.bar(
            df_players,
            x="player_name",
            y="sporta_score",
            labels={"player_name": "Player Name", "sporta_score": "SPORTA Score"},
            title="Top 10 Players by SPORTA Score"
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8'
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Player chart error: {e}")

with chart_col2:
    try:
        df_goals = pd.read_sql("""
            SELECT player_name, goals
            FROM vw_top_goal_scorers
            ORDER BY goals DESC
            LIMIT 10;
        """, engine)

        fig2 = px.bar(
            df_goals,
            x="player_name",
            y="goals",
            labels={"player_name": "Player Name", "goals": "Goals"},
            title="Top 10 Goal Scorers"
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8'
        )
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Goal chart error: {e}")

# -----------------------------------
# Team Performance Table (Top 10)
# -----------------------------------
try:
    df_team = pd.read_sql("""
        SELECT *
        FROM vw_team_performance
        ORDER BY goals DESC
        LIMIT 10;
    """, engine)

    st.subheader("🏟️ Team Performance (Top 10)")
    st.dataframe(df_team, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Team performance error: {e}")

st.divider()
st.success("✅ SPORTA VISTA PRO Executive Dashboard Loaded Successfully")
