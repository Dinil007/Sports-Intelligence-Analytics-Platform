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
from sqlalchemy import text

from database.db_connection import engine
from services.player_service import get_player_profile
from ai.response_generator import generate_scouting_verdict


# ---------------------------------------------------------------------------
# Cached data fetchers
# ---------------------------------------------------------------------------

@st.cache_data(ttl=300, show_spinner=False)
def load_player_names() -> list[str]:
    """All qualified player names from vw_scouting (≥3 matches)."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT DISTINCT player_name FROM vw_scouting ORDER BY player_name;")
        ).fetchall()
    return [r[0] for r in rows]


@st.cache_data(ttl=300, show_spinner=False)
def load_profile(player_name: str) -> dict:
    """Cached profile fetch — avoids re-querying on every Streamlit rerun."""
    return get_player_profile(player_name)


@st.cache_data(ttl=300, show_spinner=False)
def load_comparison_df(p1: str, p2: str) -> pd.DataFrame:
    """Fetch scouting stats for two players."""
    q = text("""
        SELECT *
        FROM vw_scouting
        WHERE player_name IN (:p1, :p2)
        ORDER BY sporta_score DESC;
    """)
    with engine.connect() as conn:
        return pd.read_sql(q, conn, params={"p1": p1, "p2": p2})


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

PROFILE_CARD_CSS = """
<style>
/* ── Layout grid ─────────────────────────────── */
.sp-profile-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1.5rem;
    margin: 0.75rem 0 2rem;
}

/* ── Card ────────────────────────────────────── */
.sp-card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
    transition: border-color 0.2s;
}
.sp-card:hover { border-color: rgba(148, 163, 184, 0.35); }

/* ── Header row ──────────────────────────────── */
.sp-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(148, 163, 184, 0.15);
}
.sp-avatar {
    flex: 0 0 52px;
    width: 52px; height: 52px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    font-size: 1.15rem;
    font-weight: 900;
    color: #fff;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    box-shadow: 0 4px 16px rgba(14,165,233,0.35);
    letter-spacing: 1px;
}
.sp-header-info { min-width: 0; flex: 1; }
.sp-player-name {
    color: #f1f5f9;
    font-size: 1.1rem;
    font-weight: 800;
    line-height: 1.3;
    overflow-wrap: anywhere;
    margin-bottom: 4px;
}
.sp-nickname {
    color: #94a3b8;
    font-size: 0.8rem;
    font-weight: 600;
    font-style: italic;
}

/* ── Tier badge ──────────────────────────────── */
.sp-tier-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
}
.sp-tier-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #fff;
}
.sp-score-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(148, 163, 184, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.2);
    color: #e2e8f0;
    font-size: 0.8rem;
    font-weight: 700;
}
.sp-score-label { color: #94a3b8; font-weight: 600; font-size: 0.75rem; }

/* ── Info fields ─────────────────────────────── */
.sp-fields { display: flex; flex-direction: column; gap: 0; }
.sp-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1rem;
    padding: 8px 0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.08);
}
.sp-row:last-child { border-bottom: none; padding-bottom: 0; }
.sp-label {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    flex-shrink: 0;
}
.sp-value {
    color: #e2e8f0;
    font-size: 0.88rem;
    font-weight: 700;
    text-align: right;
    overflow-wrap: anywhere;
}
.sp-value.na { color: #475569; font-weight: 500; font-style: italic; }

/* ── Stat chips row ──────────────────────────── */
.sp-stat-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    padding-top: 0.5rem;
    border-top: 1px solid rgba(148, 163, 184, 0.1);
}
.sp-stat-chip {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 6px 12px;
    background: rgba(148, 163, 184, 0.07);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 10px;
    min-width: 56px;
}
.sp-stat-chip-val { color: #f1f5f9; font-size: 0.95rem; font-weight: 800; }
.sp-stat-chip-lbl { color: #64748b; font-size: 0.65rem; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 0.5px; }

/* ── Jersey badge ────────────────────────────── */
.sp-jersey {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(14,165,233,0.12);
    border: 1px solid rgba(14,165,233,0.25);
    color: #38bdf8;
    font-size: 0.75rem;
    font-weight: 800;
    padding: 2px 10px;
    border-radius: 999px;
}

/* ── Responsive ──────────────────────────────── */
@media (max-width: 860px) {
    .sp-profile-grid { grid-template-columns: 1fr; }
}
@media (max-width: 520px) {
    .sp-card { padding: 1rem; border-radius: 14px; }
}
</style>
"""


# ---------------------------------------------------------------------------
# Profile card builder
# ---------------------------------------------------------------------------

def _esc(v) -> str:
    return html.escape(str(v))


def _field_html(label: str, value, na_val="N/A") -> str:
    is_na = (str(value).strip() == na_val)
    cls = "sp-value na" if is_na else "sp-value"
    return (
        f'<div class="sp-row">'
        f'<span class="sp-label">{_esc(label)}</span>'
        f'<span class="{cls}">{_esc(value)}</span>'
        f'</div>'
    )


def _stat_chip(label: str, value) -> str:
    return (
        f'<div class="sp-stat-chip">'
        f'<span class="sp-stat-chip-val">{_esc(value)}</span>'
        f'<span class="sp-stat-chip-lbl">{_esc(label)}</span>'
        f'</div>'
    )


def build_profile_card(profile: dict) -> str:
    name     = profile["player_name"]
    nickname = profile["nickname"]
    jersey   = profile["jersey_number"]
    tier     = profile["sporta_tier"]
    score    = profile["sporta_score"]

    # Initials avatar
    initials = "".join(p[:1] for p in name.split()[:2]).upper() or "P"

    # Nickname sub-line
    nick_html = ""
    if nickname != "N/A":
        nick_html = f'<div class="sp-nickname">"{_esc(nickname)}"</div>'

    # Jersey badge
    jersey_html = ""
    if jersey != "N/A":
        jersey_html = f'<span class="sp-jersey">#{_esc(jersey)}</span>'

    # Tier + score row
    tier_row = (
        f'<div class="sp-tier-row">'
        f'  <span class="sp-tier-badge" style="background:{_esc(tier["color"])};">'
        f'    ⭐ {_esc(tier["label"])}'
        f'  </span>'
        f'  <span class="sp-score-pill">'
        f'    <span class="sp-score-label">SPORTA</span> {_esc(score)}'
        f'  </span>'
        f'  {jersey_html}'
        f'</div>'
    )

    # Info fields
    fields_html = "".join([
        _field_html("Club / Team",    profile["team"]),
        _field_html("Nationality",    profile["nationality"]),
        _field_html("Position",       profile["position"]),
        _field_html("Age",            profile["age"]),
        _field_html("Height",         profile["height"]),
        _field_html("Preferred Foot", profile["preferred_foot"]),
        _field_html("Matches Played", profile["matches_played"]),
    ])

    # Stat chips
    chips_html = "".join([
        _stat_chip("Goals",     profile["goals"]),
        _stat_chip("xG",        profile["total_xg"]),
        _stat_chip("Dribbles",  profile["dribbles"]),
        _stat_chip("Recoveries",profile["recoveries"]),
        _stat_chip("Pressures", profile["pressures"]),
    ])

    return f"""
    <section class="sp-card">
        <div class="sp-header">
            <div class="sp-avatar">{_esc(initials)}</div>
            <div class="sp-header-info">
                <div class="sp-player-name">{_esc(name)}</div>
                {nick_html}
            </div>
        </div>
        {tier_row}
        <div class="sp-fields">{fields_html}</div>
        <div class="sp-stat-row">{chips_html}</div>
    </section>
    """


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------

st.title("⚽ SPORTA VISTA PRO – Player Comparison")

with st.spinner("Loading player list..."):
    players = load_player_names()

if len(players) < 2:
    st.error("Not enough qualified players found. At least 3 matches required.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    player1 = st.selectbox("Select Player 1", players, key="p1")
with col2:
    player2 = st.selectbox("Select Player 2", players, index=1, key="p2")

if st.button("🔍 Compare Players", type="primary", use_container_width=True):

    if player1 == player2:
        st.warning("Please select two different players.")
        st.stop()

    # ── Fetch data ─────────────────────────────────────────────────────────
    with st.spinner(f"Loading profiles for {player1} & {player2}..."):
        profile1 = load_profile(player1)
        profile2 = load_profile(player2)
        df       = load_comparison_df(player1, player2)

    if df.empty:
        st.error("No comparison data found for the selected players.")
        st.stop()

    # Align df rows to match profile1 / profile2 order
    p1_row = df[df["player_name"] == player1]
    p2_row = df[df["player_name"] == player2]
    has_p1 = not p1_row.empty
    has_p2 = not p2_row.empty

    player1_stats = p1_row.iloc[0] if has_p1 else df.iloc[0]
    player2_stats = p2_row.iloc[0] if has_p2 else df.iloc[1]

    # ── Raw stats table ─────────────────────────────────────────────────────
    st.subheader("📊 Statistics Overview")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Rich Profile Cards ──────────────────────────────────────────────────
    st.subheader("🏟️ Player Profiles")
    st.markdown(PROFILE_CARD_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="sp-profile-grid">
            {build_profile_card(profile1)}
            {build_profile_card(profile2)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPI Metrics ─────────────────────────────────────────────────────────
    st.subheader("🏆 Key Performance Indicators")
    col1, col2 = st.columns(2)

    with col1:
        s1 = float(player1_stats["sporta_score"]) if "sporta_score" in df.columns else 0.0
        tier1 = profile1["sporta_tier"]
        st.markdown(f"### {profile1['player_name']}")
        st.metric("SPORTA Score (0–100)", f"{s1:.2f}")
        st.markdown(
            f'<span style="background:{tier1["color"]};color:#fff;padding:3px 12px;'
            f'border-radius:12px;font-size:0.82rem;font-weight:700;">{tier1["label"]}</span>',
            unsafe_allow_html=True,
        )
        st.metric("Matches Played", profile1["matches_played"])
        st.metric("Goals",          profile1["goals"])
        st.metric("xG",             profile1["total_xg"])
        st.metric("Passes",         profile1["passes"])
        st.metric("Dribbles",       profile1["dribbles"])

    with col2:
        s2 = float(player2_stats["sporta_score"]) if "sporta_score" in df.columns else 0.0
        tier2 = profile2["sporta_tier"]
        st.markdown(f"### {profile2['player_name']}")
        st.metric("SPORTA Score (0–100)", f"{s2:.2f}", delta=f"{s2 - s1:+.2f}")
        st.markdown(
            f'<span style="background:{tier2["color"]};color:#fff;padding:3px 12px;'
            f'border-radius:12px;font-size:0.82rem;font-weight:700;">{tier2["label"]}</span>',
            unsafe_allow_html=True,
        )
        st.metric("Matches Played", profile2["matches_played"])
        st.metric("Goals",          profile2["goals"])
        st.metric("xG",             profile2["total_xg"])
        st.metric("Passes",         profile2["passes"])
        st.metric("Dribbles",       profile2["dribbles"])

    # ── SPORTA Score bar ─────────────────────────────────────────────────────
    st.subheader("📊 SPORTA Score Comparison (0–100)")
    score_df = pd.DataFrame({
        "Player":       [profile1["player_name"], profile2["player_name"]],
        "SPORTA Score": [s1, s2],
    }).set_index("Player")
    st.bar_chart(score_df)

    # ── Raw stats side-by-side ───────────────────────────────────────────────
    st.subheader("📊 Raw Stats Side-by-Side")
    raw_df = pd.DataFrame({
        "Metric": ["Goals", "Dribbles", "Recoveries", "Pressures"],
        profile1["player_name"]: [
            profile1["goals"], profile1["dribbles"],
            profile1["recoveries"], profile1["pressures"],
        ],
        profile2["player_name"]: [
            profile2["goals"], profile2["dribbles"],
            profile2["recoveries"], profile2["pressures"],
        ],
    }).set_index("Metric")
    st.bar_chart(raw_df)

    # ── Detailed stats expandables ───────────────────────────────────────────
    st.subheader("🔍 Detailed Statistics")
    p1n = profile1["player_name"]
    p2n = profile2["player_name"]

    def safe_val(stats, col):
        if col in df.columns and pd.notnull(stats[col]):
            return stats[col]
        return "—"

    with st.expander("⚽ Attacking Statistics"):
        st.dataframe(pd.DataFrame({
            "Metric": ["Goals", "Shots", "xG"],
            p1n: [
                safe_val(player1_stats, "goals"),
                safe_val(player1_stats, "shots"),
                safe_val(player1_stats, "total_xg"),
            ],
            p2n: [
                safe_val(player2_stats, "goals"),
                safe_val(player2_stats, "shots"),
                safe_val(player2_stats, "total_xg"),
            ],
        }).set_index("Metric"), use_container_width=True)

    with st.expander("🎯 Passing & Creativity"):
        st.dataframe(pd.DataFrame({
            "Metric": ["Total Passes", "Dribbles", "Carries"],
            p1n: [
                safe_val(player1_stats, "passes"),
                safe_val(player1_stats, "dribbles"),
                safe_val(player1_stats, "carries"),
            ],
            p2n: [
                safe_val(player2_stats, "passes"),
                safe_val(player2_stats, "dribbles"),
                safe_val(player2_stats, "carries"),
            ],
        }).set_index("Metric"), use_container_width=True)

    with st.expander("🛡️ Defensive Statistics"):
        st.dataframe(pd.DataFrame({
            "Metric": ["Pressures", "Recoveries"],
            p1n: [
                safe_val(player1_stats, "pressures"),
                safe_val(player1_stats, "recoveries"),
            ],
            p2n: [
                safe_val(player2_stats, "pressures"),
                safe_val(player2_stats, "recoveries"),
            ],
        }).set_index("Metric"), use_container_width=True)

    # ── Radar Chart ──────────────────────────────────────────────────────────
    RADAR_CAPS = {
        "sporta_score": 100.0,
        "goals":        50.0,
        "total_xg":     40.0,
        "shots":       500.0,
        "passes":    25000.0,
        "dribbles":   1000.0,
        "carries":   15000.0,
        "pressures":  3000.0,
        "recoveries": 1000.0,
    }
    radar_labels = ["SPORTA", "Goals", "xG", "Shots",
                    "Passes", "Dribbles", "Carries", "Pressures", "Recoveries"]
    radar_cols   = ["sporta_score", "goals", "total_xg", "shots",
                    "passes", "dribbles", "carries", "pressures", "recoveries"]

    avail = [(lbl, col) for lbl, col in zip(radar_labels, radar_cols) if col in df.columns]

    if len(df) >= 2 and len(avail) >= 3:
        labels = [x[0] for x in avail]
        cols   = [x[1] for x in avail]
        fig    = go.Figure()
        for _, row in df.iterrows():
            vals = [
                min(float(row[c]) / RADAR_CAPS.get(c, 1.0) * 100, 100.0)
                if pd.notnull(row[c]) else 0.0
                for c in cols
            ]
            vals.append(vals[0])
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=labels + [labels[0]],
                fill="toself", name=row["player_name"],
            ))
        fig.update_layout(
            title="Radar Comparison (Normalized 0–100)",
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
        )
        st.subheader("🕸️ Radar Chart")
        st.plotly_chart(fig, use_container_width=True)

    # ── Export ───────────────────────────────────────────────────────────────
    st.subheader("📤 Export")
    ex1, ex2, ex3 = st.columns(3)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    with ex1:
        st.download_button(
            "📄 Download CSV",
            data=csv_buffer.getvalue().encode("utf-8"),
            file_name=f"{player1}_vs_{player2}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with ex2:
        if st.button("📑 Download PDF", use_container_width=True):
            st.toast("PDF export coming soon!", icon="🚧")

    # ── AI Scouting Verdict ──────────────────────────────────────────────────
    st.subheader("🤖 AI Scouting Verdict")
    verdict = None
    try:
        with st.spinner("Generating AI scouting verdict..."):
            verdict = generate_scouting_verdict(
                player1=player1,
                player2=player2,
                dataframe_text=df.to_string(index=False),
            )
        st.markdown(verdict)
    except Exception as e:
        st.warning(f"AI verdict unavailable: {e}")

    with ex3:
        if st.button("📋 Copy AI Summary", use_container_width=True):
            if verdict:
                escaped = verdict.replace("`", "'").replace("\\", "\\\\").replace("\n", "\\n")
                components.html(
                    f"<script>navigator.clipboard.writeText(`{escaped}`);</script>",
                    height=0,
                )
                st.toast("✅ AI summary copied!", icon="📋")
            else:
                st.toast("⚠️ Generate the verdict first.", icon="⚠️")