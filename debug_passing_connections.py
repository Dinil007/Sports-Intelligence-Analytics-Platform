import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from dashboards.components.passing_network.passing_connections import render_passing_connections
from services.match_intelligence_service import get_match_dashboard

match_id = 4020846
match_dashboard = get_match_dashboard(match_id)
events = match_dashboard.get("events", [])

# Reproduce ONLY the Plotly figure creation from render_passing_connections()
# Minimal subset to trigger fig.update_layout(...)
if not events:
    print("No events available.")
    sys.exit(0)

# Import internal helper to get connections
from services.passing_network_service import calculate_passing_connections
connections = calculate_passing_connections(events)
if not connections:
    print("No connections found.")
    sys.exit(0)

teams = list(connections.keys())
selected_team = teams[0]
team_connections = connections.get(selected_team, [])[:10]

import plotly.graph_objects as go

combo_labels = []
pass_counts = []
for conn in reversed(team_connections):
    p1 = conn["passer"].split()[-1] if len(conn["passer"].split()) > 1 else conn["passer"]
    p2 = conn["receiver"].split()[-1] if len(conn["receiver"].split()) > 1 else conn["receiver"]
    combo_labels.append(f"{p1} → {p2}")
    pass_counts.append(conn["count"])

fig = go.Figure()
fig.add_trace(
    go.Bar(
        y=combo_labels,
        x=pass_counts,
        orientation="h",
        marker=dict(
            color=pass_counts,
            colorscale="Viridis",
            line=dict(color="white", width=1),
        ),
        text=pass_counts,
        textposition="auto",
        hovertemplate="Combination: %{y}<br>Passes: %{x}<extra></extra>",
    )
)

print("Attempting fig.update_layout(...)")
try:
    fig.update_layout(
        title=dict(
            text=f"Top 10 Passing Combinations: {selected_team}",
            font=dict(color="white", size=16),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title=dict(
                text="Number of Passes",
                font=dict(color="white"),
            ),
            tickfont=dict(color="white"),
            gridcolor="rgba(255, 255, 255, 0.1)",
        ),
        yaxis=dict(
            tickfont=dict(color="white"),
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=150, r=20, t=50, b=50),
        height=400,
    )
except Exception as e:
    import traceback
    traceback.print_exc()