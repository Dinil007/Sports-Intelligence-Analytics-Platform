import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import html
import io
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

from database.db_connection import engine
from ai.response_generator import explain_results, generate_scouting_verdict


# ---------------------------------------------------------------------------
# Tier helper
# ---------------------------------------------------------------------------
def sporta_tier(score: float) -> tuple[str, str]:
    """Return (label, hex_colour) for a normalized SPORTA Score."""
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

# Page Config handled by central entry point app.py

st.title("⚽ SPORTA VISTA PRO - Player Comparison")

# Load player names
players_query = """
SELECT DISTINCT player_name
FROM vw_scouting
ORDER BY player_name;
"""

players = pd.read_sql(players_query, engine)["player_name"].tolist()

if len(players) < 2:
    st.error("Not enough players found in vw_scouting.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    player1 = st.selectbox("Select Player 1", players)

with col2:
    player2 = st.selectbox(
        "Select Player 2",
        players,
        index=1 if len(players) > 1 else 0
    )

if st.button("🔍 Compare Players"):

    if player1 == player2:
        st.warning("Please select two different players.")
        st.stop()

    query = f"""
    SELECT *
    FROM vw_scouting
    WHERE player_name IN ('{player1}', '{player2}');
    """

    df = pd.read_sql(query, engine)

    st.subheader("📊 Player Statistics")
    st.dataframe(df, use_container_width=True)

    # ----------------------------
    # KPI Cards
    # ----------------------------

    # Get each player's row
    player1_stats = df.iloc[0]
    player2_stats = df.iloc[1]

    # ----------------------------
    # Player Profile Cards
    # ----------------------------

    st.markdown(
        """
        <style>
        .sporta-profile-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1.25rem;
            align-items: stretch;
            margin: 0.5rem 0 1.75rem;
        }
        .sporta-player-card {
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
            background: linear-gradient(145deg, #111827 0%, #172033 100%);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 18px;
            padding: 1.35rem;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.28);
        }
        .sporta-card-header {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            padding-bottom: 0.85rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.18);
        }
        .sporta-avatar {
            flex: 0 0 44px;
            width: 44px;
            height: 44px;
            border-radius: 14px;
            display: grid;
            place-items: center;
            background: #0ea5e9;
            color: #f8fafc;
            font-weight: 800;
            font-size: 1rem;
        }
        .sporta-player-name {
            min-width: 0;
            color: #f8fafc;
            font-size: 1.12rem;
            line-height: 1.35;
            font-weight: 800;
            overflow-wrap: anywhere;
        }
        .sporta-profile-fields {
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
        }
        .sporta-profile-row {
            display: grid;
            grid-template-columns: minmax(8.5rem, 0.8fr) minmax(0, 1.2fr);
            gap: 1rem;
            align-items: start;
            padding-bottom: 0.65rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        }
        .sporta-profile-row:last-child {
            border-bottom: 0;
            padding-bottom: 0;
        }
        .sporta-profile-label {
            color: #94a3b8;
            font-size: 0.82rem;
            font-weight: 650;
            line-height: 1.35;
        }
        .sporta-profile-value {
            color: #e5e7eb;
            font-size: 0.92rem;
            line-height: 1.4;
            font-weight: 700;
            overflow-wrap: anywhere;
            text-align: right;
        }
        .sporta-profile-value.is-empty {
            color: #64748b;
            font-style: italic;
            font-weight: 600;
        }
        @media (max-width: 900px) {
            .sporta-profile-grid {
                grid-template-columns: 1fr;
            }
        }
        @media (max-width: 560px) {
            .sporta-player-card {
                padding: 1rem;
                border-radius: 14px;
            }
            .sporta-profile-row {
                grid-template-columns: 1fr;
                gap: 0.25rem;
            }
            .sporta-profile-value {
                text-align: left;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def profile_field(stats, col, label, default="-"):
        """Return a profile row HTML string; shows default if column absent or null."""
        value = default
        is_empty = True
        if col in df.columns:
            raw_value = stats[col]
            if pd.notnull(raw_value) and str(raw_value).strip() not in ("", "None"):
                value = raw_value
                is_empty = False

        value_class = "sporta-profile-value is-empty" if is_empty else "sporta-profile-value"
        return (
            '<div class="sporta-profile-row">'
            f'<span class="sporta-profile-label">{html.escape(label)}</span>'
            f'<span class="{value_class}">{html.escape(str(value))}</span>'
            '</div>'
        )

    def build_card(stats):
        name = str(stats["player_name"])
        initials = "".join(part[:1] for part in name.split()[:2]).upper() or "P"
        rows = "".join([
            profile_field(stats, "position", "Position"),
            profile_field(stats, "nationality", "Nationality"),
            profile_field(stats, "team", "Club / Team"),
            profile_field(stats, "club", "Club"),
            profile_field(stats, "age", "Age"),
            profile_field(stats, "preferred_foot", "Preferred Foot"),
        ])
        return (
            '<section class="sporta-player-card">'
            '<div class="sporta-card-header">'
            f'<div class="sporta-avatar">{html.escape(initials)}</div>'
            f'<div class="sporta-player-name">{html.escape(name)}</div>'
            '</div>'
            f'<div class="sporta-profile-fields">{rows}</div>'
            '</section>'
        )

    st.subheader("Player Profiles")
    st.markdown(
        f"""
        <div class="sporta-profile-grid">
            {build_card(player1_stats)}
            {build_card(player2_stats)}
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.subheader("🏆 Key Performance Indicators")

    col1, col2 = st.columns(2)

    with col1:
        s1 = float(player1_stats["sporta_score"])
        tier1_label, tier1_color = sporta_tier(s1)
        st.markdown(f"### {player1_stats['player_name']}")
        st.metric("SPORTA Score (0–100)", f"{s1:.2f}")
        st.markdown(
            f'<span style="background:{tier1_color};color:#fff;padding:3px 12px;'
            f'border-radius:12px;font-size:0.82rem;font-weight:700;">{tier1_label}</span>',
            unsafe_allow_html=True,
        )
        st.metric("Matches Played", int(player1_stats["matches_played"]) if "matches_played" in df.columns else "—")
        st.metric("Goals", player1_stats["goals"])
        st.metric("xG", round(float(player1_stats["total_xg"]), 2))
        st.metric("Passes", player1_stats["passes"])
        st.metric("Dribbles", player1_stats["dribbles"])

    with col2:
        s2 = float(player2_stats["sporta_score"])
        tier2_label, tier2_color = sporta_tier(s2)
        st.markdown(f"### {player2_stats['player_name']}")
        st.metric(
            "SPORTA Score (0–100)",
            f"{s2:.2f}",
            delta=f"{s2 - s1:+.2f}",
        )
        st.markdown(
            f'<span style="background:{tier2_color};color:#fff;padding:3px 12px;'
            f'border-radius:12px;font-size:0.82rem;font-weight:700;">{tier2_label}</span>',
            unsafe_allow_html=True,
        )
        st.metric("Matches Played", int(player2_stats["matches_played"]) if "matches_played" in df.columns else "—")
        st.metric("Goals", player2_stats["goals"])
        st.metric("xG", round(float(player2_stats["total_xg"]), 2))
        st.metric("Passes", player2_stats["passes"])
        st.metric("Dribbles", player2_stats["dribbles"])

    # ----------------------------
    # SPORTA Score comparison bar (separate from raw stats)
    # ----------------------------
    st.subheader("📊 SPORTA Score Comparison (0–100)")
    score_df = pd.DataFrame({
        "Player": [player1_stats["player_name"], player2_stats["player_name"]],
        "SPORTA Score": [s1, s2],
    }).set_index("Player")
    st.bar_chart(score_df, y_label="Score (0–100)")

    # ----------------------------
    # Side-by-Side Raw Stats Bar Chart
    # ----------------------------
    chart_df = pd.DataFrame({
        "Metric": ["Goals", "Dribbles", "Recoveries", "Pressures"],
        player1_stats["player_name"]: [
            player1_stats["goals"],
            player1_stats["dribbles"],
            player1_stats["recoveries"],
            player1_stats["pressures"],
        ],
        player2_stats["player_name"]: [
            player2_stats["goals"],
            player2_stats["dribbles"],
            player2_stats["recoveries"],
            player2_stats["pressures"],
        ],
    }).set_index("Metric")

    st.subheader("📊 Raw Stats Side-by-Side")
    st.bar_chart(chart_df)

    # ----------------------------
    # Detailed Stats by Category
    # ----------------------------

    st.subheader("🔍 Detailed Statistics")

    p1 = player1_stats["player_name"]
    p2 = player2_stats["player_name"]

    def safe_val(stats, col, fmt=None):
        """Return formatted value if column exists, else '—'."""
        if col in df.columns and pd.notnull(stats[col]):
            val = stats[col]
            if fmt == "pct":
                return f"{round(float(val) * 100, 1)}%"
            if fmt == "round2":
                return round(float(val), 2)
            return val
        return "—"

    # ⚽ Attacking
    with st.expander("⚽ Attacking Statistics"):
        attacking_data = {
            "Metric": ["Goals", "Shots", "xG", "Shot Conversion Rate"],
            p1: [
                safe_val(player1_stats, "goals"),
                safe_val(player1_stats, "shots"),
                safe_val(player1_stats, "total_xg", "round2"),
                safe_val(player1_stats, "shot_conversion_rate", "pct"),
            ],
            p2: [
                safe_val(player2_stats, "goals"),
                safe_val(player2_stats, "shots"),
                safe_val(player2_stats, "total_xg", "round2"),
                safe_val(player2_stats, "shot_conversion_rate", "pct"),
            ],
        }
        st.dataframe(pd.DataFrame(attacking_data).set_index("Metric"), use_container_width=True)

    # 🎯 Passing & Creativity
    with st.expander("🎯 Passing & Creativity"):
        passing_data = {
            "Metric": ["Total Passes", "Pass Completion %", "Assists", "Key Passes"],
            p1: [
                safe_val(player1_stats, "passes"),
                safe_val(player1_stats, "pass_completion_pct", "pct"),
                safe_val(player1_stats, "assists"),
                safe_val(player1_stats, "key_passes"),
            ],
            p2: [
                safe_val(player2_stats, "passes"),
                safe_val(player2_stats, "pass_completion_pct", "pct"),
                safe_val(player2_stats, "assists"),
                safe_val(player2_stats, "key_passes"),
            ],
        }
        st.dataframe(pd.DataFrame(passing_data).set_index("Metric"), use_container_width=True)

    # 👟 Ball Progression
    with st.expander("👟 Ball Progression"):
        progression_data = {
            "Metric": ["Dribbles", "Carries", "Progressive Carries"],
            p1: [
                safe_val(player1_stats, "dribbles"),
                safe_val(player1_stats, "carries"),
                safe_val(player1_stats, "progressive_carries"),
            ],
            p2: [
                safe_val(player2_stats, "dribbles"),
                safe_val(player2_stats, "carries"),
                safe_val(player2_stats, "progressive_carries"),
            ],
        }
        st.dataframe(pd.DataFrame(progression_data).set_index("Metric"), use_container_width=True)

    # 🛡️ Defensive
    with st.expander("🛡️ Defensive Statistics"):
        defensive_data = {
            "Metric": ["Pressures", "Recoveries", "Tackles", "Interceptions"],
            p1: [
                safe_val(player1_stats, "pressures"),
                safe_val(player1_stats, "recoveries"),
                safe_val(player1_stats, "tackles"),
                safe_val(player1_stats, "interceptions"),
            ],
            p2: [
                safe_val(player2_stats, "pressures"),
                safe_val(player2_stats, "recoveries"),
                safe_val(player2_stats, "tackles"),
                safe_val(player2_stats, "interceptions"),
            ],
        }
        st.dataframe(pd.DataFrame(defensive_data).set_index("Metric"), use_container_width=True)

    # ----------------------------
    # Radar Chart
    # ----------------------------

    # ----------------------------
    # Radar Chart — use normalized (0–1) values so all axes share the same scale
    # ----------------------------
    # Elite benchmarks (per match) — same as the SQL formula caps
    RADAR_CAPS = {
        "sporta_score": 100.0,   # already 0–100
        "goals":        50.0,    # career goals cap for radar
        "total_xg":     40.0,    # career xG cap
        "shots":       500.0,    # career shots cap
        "passes":    25000.0,    # career passes cap
        "dribbles":   1000.0,    # career dribbles cap
        "carries":   15000.0,    # career carries cap
        "pressures":  3000.0,    # career pressures cap
        "recoveries": 1000.0,    # career recoveries cap
    }

    radar_labels = ["SPORTA Score", "Goals", "xG", "Shots",
                    "Passes", "Dribbles", "Carries", "Pressures", "Recoveries"]
    radar_cols   = ["sporta_score", "goals", "total_xg", "shots",
                    "passes", "dribbles", "carries", "pressures", "recoveries"]

    available_radar = [(lbl, col) for lbl, col in zip(radar_labels, radar_cols) if col in df.columns]

    if len(df) == 2 and len(available_radar) >= 3:
        labels = [x[0] for x in available_radar]
        cols   = [x[1] for x in available_radar]

        fig = go.Figure()

        for _, row in df.iterrows():
            values = []
            for col in cols:
                raw = float(row[col]) if pd.notnull(row[col]) else 0.0
                cap = RADAR_CAPS.get(col, 1.0)
                values.append(min(raw / cap * 100, 100.0))   # 0–100 scale

            values.append(values[0])  # close polygon

            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=labels + [labels[0]],
                    fill="toself",
                    name=row["player_name"],
                )
            )

        fig.update_layout(
            title="Player Radar Comparison (Normalized 0–100)",
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
        )

        st.subheader("🕸️ Radar Chart")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Export
    # ----------------------------

    st.subheader("📤 Export")

    export_col1, export_col2, export_col3 = st.columns(3)

    # --- CSV Download ---
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    with export_col1:
        st.download_button(
            label="📄 Download CSV",
            data=csv_bytes,
            file_name=f"{player1}_vs_{player2}_comparison.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # --- PDF (Coming Soon) ---
    with export_col2:
        if st.button("📑 Download PDF", use_container_width=True):
            st.toast("📑 PDF export coming soon!", icon="🚧")

    # --- AI Scouting Verdict + Copy ---
    # ----------------------------
    # AI Scouting Verdict
    # ----------------------------

    st.subheader("🤖 AI Scouting Verdict")

    verdict = None

    try:
        with st.spinner("Generating scouting verdict..."):
            verdict = generate_scouting_verdict(
                player1=player1,
                player2=player2,
                dataframe_text=df.to_string(index=False),
            )

        st.markdown(verdict)

    except Exception as e:
        st.warning(f"AI verdict unavailable: {e}")

    # --- Copy AI Summary ---
    with export_col3:
        if st.button("📋 Copy AI Summary", use_container_width=True):
            if verdict:
                # Inject JS to copy to clipboard
                escaped = verdict.replace("`", "'").replace("\\", "\\\\").replace("\n", "\\n")
                components.html(
                    f"""
                    <script>
                    navigator.clipboard.writeText(`{escaped}`).then(function() {{
                        console.log('Copied to clipboard');
                    }});
                    </script>
                    """,
                    height=0,
                )
                st.toast("✅ AI summary copied to clipboard!", icon="📋")
            else:
                st.toast("⚠️ Generate the verdict first.", icon="⚠️")