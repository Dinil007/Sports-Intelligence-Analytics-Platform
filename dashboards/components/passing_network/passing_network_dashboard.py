"""
dashboards/components/passing_network/passing_network_dashboard.py
=====================================================================
Master orchestrator for the Passing Network & Team Shape Analytics section.

No calculations here. Only layout and structure.
Calls every visualization exactly once in the specified layout order.
"""

from __future__ import annotations

from typing import Any
import streamlit as st

# Import the service helper to retrieve passing events
from services.passing_network_service import get_passing_events

# Import all component renderers
from dashboards.components.passing_network.passing_network_chart import (
    render_passing_network,
)
from dashboards.components.passing_network.average_positions import (
    render_average_positions,
)
from dashboards.components.passing_network.passing_connections import (
    render_passing_connections,
)
from dashboards.components.passing_network.network_kpis import render_network_kpis
from dashboards.components.passing_network.passing_zones import (
    render_passing_zones,
)
from dashboards.components.passing_network.progressive_network import (
    render_progressive_network,
)
from dashboards.components.passing_network.formation_detector import (
    render_detected_formation,
)
from dashboards.components.passing_network.team_shape import render_team_shape


def render_passing_network_dashboard(match_dashboard: dict[str, Any]) -> None:
    """Orchestrate and lay out the Passing Network & Team Shape Analytics dashboard section.

    Parameters
    ----------
    match_dashboard : dict
        The full match intelligence dashboard data package.
    """
    # Call the service layer to get cleaned passing events
    events = get_passing_events(match_dashboard)

    st.markdown("## âš½ Passing Network & Team Shape Analytics")

    # 1. Passing Network
    render_passing_network(events)
    st.divider()

    # 2. Average Positions
    render_average_positions(events)
    st.divider()

    # 3. Passing Connections
    # render_passing_connections(events)
    st.divider()

    # 4. Network KPIs
    render_network_kpis(events)
    st.divider()

    # 5. Passing Zones
    render_passing_zones(events)
    st.divider()

    # 6. Progressive Passing
    render_progressive_network(events)
    st.divider()

    # 7. Detected Formation
    render_detected_formation(events)
    st.divider()

    # 8. Team Shape
    render_team_shape(events)
