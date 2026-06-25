"""
dashboards/pages/8_Player_Comparison.py
=========================================
SPORTA VISTA PRO – Player Comparison with rich profile cards.

Architecture:
  UI (this file)
    ↓
  services/player_service.py   ← clean business logic
    ↓
  database/player_repository.py ← all SQL lives here
"""

import sys
import io
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import html
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

from database.player_repository import fetch_player_name_list
from services.player_service import get_player_profile

# Page Config handled by central entry point app.py

# ============================================================
# CSS – professional dark cards
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* ---------- Profile grid ---------- */
.svp-profile-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin: 1.25rem 0 2rem;
}
@media (max-width: 860px) {
    .svp-profile-grid { grid-template-columns: 1fr; }
}

/* ---------- Card shell ---------- */
.svp-card {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 24px 48px -12px rgba(0,0,0,0.55);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    min-width: 0;
}

/* ---------- Card header ---------- */
.svp-card-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(148,163,184,0.15);
}
.svp-avatar {
    flex: 0 0 52px;
    width: 52px;
    height: 52px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    color: #fff;
    font-weight: 900;
    font-size: 1.15rem;
    letter-spacing: 1px;
    box-shadow: 0 4px 14px rgba(14,165,233,0.35);
}
.svp-header-text { min-width: 0; }
.svp-player-display-name {
    color: #f1f5f9;
    font-size: 1.18rem;
    font-weight: 800;
    line-height: 1.25;
    overflow-wrap: anywhere;
    margin: 0;
}
.svp-player-full-name {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 2px 0 6px;
    overflow-wrap: anywhere;
}

/* ---------- Tier badge ---------- */
.svp-tier-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #fff;
}

/* ---------- Profile fields ---------- */
.svp-fields { display: flex; flex-direction: column; gap: 0; }
.svp-field-row {
    display: grid;
    grid-template-columns: 9rem 1fr;
    gap: 0.75rem;
    align-items: start;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(148,163,184,0.08);
}
.svp-field-row:last-child { border-bottom: none; }
.svp-field-label {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding-top: 1px;
}
.svp-field-value {
    color: #e2e8f0;
    font-size: 0.88rem;
    font-weight: 600;
    overflow-wrap: anywhere;
    text-align: right;
}
.svp-field-value.na {
    color: #475569;
    font-style: italic;
    font-weight: 500;
}

/* ---------- Stats section ---------- */
.svp-stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-top: 0.25rem;
}
.svp-stat-chip {
    background: rgba(148,163,184,0.07);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 10px;
    padding: 0.5rem 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.svp-stat-label {
    color: #64748b;
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.svp-stat-value {
    color: #f1f5f9;
    font-size: 1rem;
    font-weight: 800;
}
.svp-stat-value.na { color: #475569; font-style: italic; font-size: 0.82rem; }

/* ---------- Section header ---------- */
.svp-section-title {
    font-family: 'Inter', sans-serif;
    color: #94a3b8;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.25rem;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# Page title
# ============================================================
st.title("⚽ SPORTA VISTA PRO — Player Comparison")
st.markdown("Select two players to compare their profiles and performance statistics.")


# ============================================================
# Player selector
# ============================================================
@st.cache_data(ttl=300, show_spinner=False)
def load_player_names() -> list[str]:
    return fetch_player_name_list()


with st.spinner("Loading player list…"):
    players = load_player_names()

if len(players) < 2:
    st.error("Not enough players found. Ensure vw_scouting has data.")
    st.stop()

sel_col1, sel_col2 = st.columns(2)
with sel_col1:
    player1_name = st.selectbox("🔵 Player 1", players, key="p1_select")
with sel_col2:
    player2_name = st.selectbox("🔴 Player 2", players,
                                index=min(1, len(players) - 1), key="p2_select")

compare_btn = st.button("🔍 Compare Players", use_container_width=True,
                        type="primary")

if not compare_btn:
    st.stop()

if player1_name == player2_name:
    st.warning("Please select two **different** players.")
    st.stop()


# ============================================================
# Load profiles (cached per player name)
# ============================================================
@st.cache_data(ttl=300, show_spinner=False)
def cached_profile(name: str) -> dict:
    return get_player_profile(name)


with st.spinner("Loading player profiles…"):
    p1 = cached_profile(player1_name)
    p2 = cached_profile(player2_name)


# ============================================================
# Card renderer
# ============================================================
def _field_row(label: str, value: str) -> str:
    is_na = value == "N/A"
    val_class = "svp-field-value na" if is_na else "svp-field-value"
    return (
        '<div class="svp-field-row">'
        f'<span class="svp-field-label">{html.escape(label)}</span>'
        f'<span class="{val_class}">{html.escape(value)}</span>'
        '</div>'
    )


def _stat_chip(label: str, value: str) -> str:
    is_na = value == "N/A"
    val_class = "svp-stat-value na" if is_na else "svp-stat-value"
    return (
        '<div class="svp-stat-chip">'
        f'<span class="svp-stat-label">{html.escape(label)}</span>'
        f'<span class="{val_class}">{html.escape(value)}</span>'
        '</div>'
    )


def render_profile_card(p: dict, accent_color: str = "#0ea5e9") -> str:
    tier_label, tier_color = p["sporta_tier"]
    score_str = f"{p['sporta_score']:.2f}" if p["sporta_score"] is not None else "N/A"

    # Profile fields (identity info — first 5 rows only in the header card)
    identity_rows = "".join(
        _field_row(lbl, val)
        for lbl, val in p["profile_fields"]
    )

    # Stats chips (performance)
    stat_chips = "".join(
        _stat_chip(lbl, val)
        for lbl, val in p["stat_fields"]
    )

    display = html.escape(p["display_name"])
    full = html.escape(p["full_name"])
    initials = html.escape(p["initials"])
    show_full = f'<p class="svp-player-full-name">{full}</p>' if full != display else ""

    return f"""
    <div class="svp-card">
        <div class="svp-card-header">
            <div class="svp-avatar">{initials}</div>
            <div class="svp-header-text">
                <p class="svp-player-display-name">{display}</p>
                {show_full}
                <span class="svp-tier-badge" style="background:{tier_color};">{tier_label}</span>
                &nbsp;
                <span style="color:#94a3b8;font-size:0.78rem;font-weight:600;">
                    SPORTA Score: <strong style="color:#f1f5f9;">{score_str}</strong>
                </span>
            </div>
        </div>

        <div>
            <p class="svp-section-title">Player Profile</p>
            <div class="svp-fields">
                {identity_rows}
            </div>
        </div>

        <div>
            <p class="svp-section-title">Performance Statistics</p>
            <div class="svp-stats-grid">
                {stat_chips}
            </div>
        </div>
    </div>
    """


# ============================================================
# Render profile cards
# ============================================================
st.markdown("---")
st.subheader("🪪 Player Profile Cards")

st.markdown(
    f"""
    <div class="svp-profile-grid">
        {render_profile_card(p1, "#0ea5e9")}
        {render_profile_card(p2, "#f43f5e")}
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SPORTA Score comparison bar
# ============================================================
st.subheader("🏆 SPORTA Score Comparison (0–100)")

s1 = p1["sporta_score"]
s2 = p2["sporta_score"]

if s1 is not None or s2 is not None:
    score_data = pd.DataFrame({
        "Player": [p1["display_name"], p2["display_name"]],
        "SPORTA Score": [s1 or 0.0, s2 or 0.0],
    }).set_index("Player")
    st.bar_chart(score_data)

    # Delta callout
    if s1 is not None and s2 is not None:
        delta = s1 - s2
        winner = p1["display_name"] if delta > 0 else p2["display_name"]
        loser  = p2["display_name"] if delta > 0 else p1["display_name"]
        st.info(
            f"**{winner}** leads by **{abs(delta):.2f} points** over {loser}."
        )
else:
    st.warning("SPORTA Score not available for these players (minimum 3 matches required).")


# ============================================================
# Raw stats side-by-side comparison table
# ============================================================
st.subheader("📊 Side-by-Side Statistics")

stat_keys = [
    ("Goals",        "goals"),
    ("xG",           "total_xg"),
    ("Passes",       "passes"),
    ("Shots",        "shots"),
    ("Dribbles",     "dribbles"),
    ("Carries",      "carries"),
    ("Pressures",    "pressures"),
    ("Recoveries",   "recoveries"),
    ("Matches",      "matches_played"),
]

def _raw_val(raw: dict, key: str):
    v = raw.get(key)
    if v is None:
        return "N/A"
    try:
        if key in ("total_xg", "sporta_score"):
            return round(float(v), 2)
        return int(float(v))
    except (TypeError, ValueError):
        return "N/A"

comparison_data = {
    "Metric": [lbl for lbl, _ in stat_keys],
    p1["display_name"]: [_raw_val(p1["raw"], k) for _, k in stat_keys],
    p2["display_name"]: [_raw_val(p2["raw"], k) for _, k in stat_keys],
}
st.dataframe(
    pd.DataFrame(comparison_data).set_index("Metric"),
    use_container_width=True,
)


# ============================================================
# Raw stats bar chart (numeric only, on comparable scale)
# ============================================================
st.subheader("📊 Raw Stats Bar Chart")

bar_keys = [("Goals","goals"), ("Dribbles","dribbles"),
            ("Recoveries","recoveries"), ("Pressures","pressures")]

bar_data = pd.DataFrame({
    "Metric": [lbl for lbl, _ in bar_keys],
    p1["display_name"]: [_raw_val(p1["raw"], k) for _, k in bar_keys],
    p2["display_name"]: [_raw_val(p2["raw"], k) for _, k in bar_keys],
}).set_index("Metric")

# Only plot numeric rows
bar_data = bar_data[bar_data.apply(
    lambda row: all(v != "N/A" for v in row), axis=1
)]
if not bar_data.empty:
    st.bar_chart(bar_data)
else:
    st.info("Not enough numeric data to render bar chart.")


# ============================================================
# Radar chart – all axes normalized 0-100
# ============================================================
RADAR_CAPS = {
    "sporta_score": 100.0,
    "goals":        60.0,
    "total_xg":     50.0,
    "shots":       500.0,
    "passes":    28000.0,
    "dribbles":   1200.0,
    "carries":   18000.0,
    "pressures":  4000.0,
    "recoveries": 1200.0,
}

RADAR_LABELS = ["SPORTA", "Goals", "xG", "Shots",
                "Passes", "Dribbles", "Carries", "Pressures", "Recoveries"]
RADAR_KEYS   = ["sporta_score", "goals", "total_xg", "shots",
                "passes", "dribbles", "carries", "pressures", "recoveries"]


def _radar_values(raw: dict) -> list[float]:
    vals = []
    for key in RADAR_KEYS:
        v = raw.get(key)
        try:
            fv = float(v) if v is not None else 0.0
        except (TypeError, ValueError):
            fv = 0.0
        cap = RADAR_CAPS.get(key, 1.0)
        vals.append(min(fv / cap * 100, 100.0))
    return vals


v1 = _radar_values(p1["raw"])
v2 = _radar_values(p2["raw"])

fig = go.Figure()
for name, values, color in [
    (p1["display_name"], v1, "#0ea5e9"),
    (p2["display_name"], v2, "#f43f5e"),
]:
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=RADAR_LABELS + [RADAR_LABELS[0]],
        fill="toself",
        name=name,
        line=dict(color=color, width=2),
        fillcolor=color.replace("#", "rgba(") + ",0.12)" if color.startswith("#") else color,
    ))

fig.update_layout(
    title=dict(text="Player Radar Comparison (Normalized 0–100)", font=dict(color="#94a3b8")),
    polar=dict(
        bgcolor="rgba(15,23,42,0.6)",
        radialaxis=dict(visible=True, range=[0, 100],
                        gridcolor="rgba(148,163,184,0.15)",
                        tickfont=dict(color="#64748b")),
        angularaxis=dict(gridcolor="rgba(148,163,184,0.15)",
                         tickfont=dict(color="#94a3b8"))
    ),
    paper_bgcolor="rgba(15,23,42,0)",
    plot_bgcolor="rgba(15,23,42,0)",
    showlegend=True,
    legend=dict(font=dict(color="#94a3b8")),
    height=450,
)

st.subheader("🕸️ Radar Chart")
st.plotly_chart(fig, use_container_width=True)


# ============================================================
# Detailed stats expanders
# ============================================================
n1, n2 = p1["display_name"], p2["display_name"]

def _safe(raw: dict, key: str, decimals: int = 0):
    v = raw.get(key)
    if v is None:
        return "—"
    try:
        if decimals:
            return f"{float(v):.{decimals}f}"
        return str(int(float(v)))
    except (TypeError, ValueError):
        return str(v)

with st.expander("⚽ Attacking Statistics"):
    st.dataframe(pd.DataFrame({
        "Metric": ["Goals", "Shots", "xG"],
        n1: [_safe(p1["raw"],"goals"), _safe(p1["raw"],"shots"), _safe(p1["raw"],"total_xg",2)],
        n2: [_safe(p2["raw"],"goals"), _safe(p2["raw"],"shots"), _safe(p2["raw"],"total_xg",2)],
    }).set_index("Metric"), use_container_width=True)

with st.expander("🎯 Passing & Creativity"):
    st.dataframe(pd.DataFrame({
        "Metric": ["Total Passes", "Dribbles", "Carries"],
        n1: [_safe(p1["raw"],"passes"), _safe(p1["raw"],"dribbles"), _safe(p1["raw"],"carries")],
        n2: [_safe(p2["raw"],"passes"), _safe(p2["raw"],"dribbles"), _safe(p2["raw"],"carries")],
    }).set_index("Metric"), use_container_width=True)

with st.expander("🛡️ Defensive Statistics"):
    st.dataframe(pd.DataFrame({
        "Metric": ["Pressures", "Recoveries"],
        n1: [_safe(p1["raw"],"pressures"), _safe(p1["raw"],"recoveries")],
        n2: [_safe(p2["raw"],"pressures"), _safe(p2["raw"],"recoveries")],
    }).set_index("Metric"), use_container_width=True)


# ============================================================
# Export
# ============================================================
st.subheader("📤 Export")

# Build export dataframe from profile fields + stat fields
export_rows: list[dict] = []
for (lbl, v1_val), (_, v2_val) in zip(p1["profile_fields"], p2["profile_fields"]):
    export_rows.append({"Field": lbl, n1: v1_val, n2: v2_val})
for (lbl, v1_val), (_, v2_val) in zip(p1["stat_fields"], p2["stat_fields"]):
    export_rows.append({"Field": lbl, n1: v1_val, n2: v2_val})

export_df = pd.DataFrame(export_rows).set_index("Field")

csv_buf = io.StringIO()
export_df.to_csv(csv_buf)

exp_col1, exp_col2, exp_col3 = st.columns(3)

with exp_col1:
    st.download_button(
        label="📄 Download CSV",
        data=csv_buf.getvalue().encode("utf-8"),
        file_name=f"{p1['display_name']}_vs_{p2['display_name']}.csv",
        mime="text/csv",
        use_container_width=True,
    )

with exp_col2:
    if st.button("📑 Download PDF", use_container_width=True):
        st.toast("📑 PDF export coming soon!", icon="🚧")


# ============================================================
# AI Scouting Verdict
# ============================================================
st.subheader("🤖 AI Scouting Verdict")

verdict = None
try:
    from ai.response_generator import generate_scouting_verdict
    # Build a compact stats string for the AI
    stats_str = export_df.to_string()
    with st.spinner("Generating AI scouting verdict…"):
        verdict = generate_scouting_verdict(
            player1=p1["display_name"],
            player2=p2["display_name"],
            dataframe_text=stats_str,
        )
    st.markdown(verdict)
except Exception as e:
    st.warning(f"AI verdict unavailable: {e}")

with exp_col3:
    if st.button("📋 Copy AI Summary", use_container_width=True):
        if verdict:
            escaped = verdict.replace("`", "'").replace("\\", "\\\\").replace("\n", "\\n")
            components.html(
                f"""
                <script>
                navigator.clipboard.writeText(`{escaped}`).then(function() {{
                    console.log('Copied');
                }});
                </script>
                """,
                height=0,
            )
            st.toast("✅ AI summary copied to clipboard!", icon="📋")
        else:
            st.toast("⚠️ Generate the verdict first.", icon="⚠️")