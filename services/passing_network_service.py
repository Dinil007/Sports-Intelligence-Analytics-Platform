"""
services/passing_network_service.py
======================================
Pure calculation service for Passing Network & Team Shape Analytics.

No Streamlit. No Plotly. No SQL. No repository imports.
All functions receive plain data structures and return calculated metrics.
"""

from __future__ import annotations

import math
from typing import Any


def get_passing_events(match_dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract and clean completed pass events from the match dashboard data.

    Parameters
    ----------
    match_dashboard : dict
        Dashboard data dictionary containing "events" list.

    Returns
    -------
    list[dict]
        Cleaned pass events with receiver information and coordinates.
    """
    events = match_dashboard.get("events", [])
    if not events:
        return []

    # Sort events chronologically to trace possession and pass outcomes
    sorted_events = sorted(
        events,
        key=lambda e: (
            e.get("period") or 1,
            e.get("minute") or 0,
            e.get("second") or 0,
        ),
    )

    passing_events = []
    for i, e in enumerate(sorted_events):
        if (
            e.get("event_type") == "Pass"
            and e.get("location") is not None
            and e.get("pass_end_location") is not None
        ):
            # Locate the receiver by scanning forward
            # In StatsBomb data, the immediate next event is usually "Ball Receipt"
            receiver_name = None
            team_name = e.get("team_name")
            player_name = e.get("player_name")

            for j in range(i + 1, min(i + 6, len(sorted_events))):
                next_event = sorted_events[j]
                
                # If team changed, the pass was intercepted/incomplete
                if next_event.get("team_name") != team_name:
                    if next_event.get("player_name"):
                        break
                    continue

                # If same team, check who received it
                next_player = next_event.get("player_name")
                if next_player and next_player != player_name:
                    receiver_name = next_player
                    break

            if receiver_name:
                passing_events.append({
                    "id": e.get("id"),
                    "player_name": player_name,
                    "receiver_name": receiver_name,
                    "team_name": team_name,
                    "location": e.get("location"),
                    "pass_end_location": e.get("pass_end_location"),
                    "minute": e.get("minute"),
                    "second": e.get("second"),
                    "period": e.get("period"),
                })

    return passing_events


def calculate_average_positions(events: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, float]]]:
    """Calculate the average coordinates of each player based on their pass events.

    Parameters
    ----------
    events : list[dict]
        Passing events from ``get_passing_events``.

    Returns
    -------
    dict
        {team_name: {player_name: {"x": float, "y": float, "count": int}}}
    """
    positions: dict[str, dict[str, dict[str, float]]] = {}
    for e in events:
        team = e.get("team_name")
        player = e.get("player_name")
        loc = e.get("location")
        if team and player and loc:
            if team not in positions:
                positions[team] = {}
            if player not in positions[team]:
                positions[team][player] = {"x_sum": 0.0, "y_sum": 0.0, "count": 0.0}
            
            positions[team][player]["x_sum"] += loc[0]
            positions[team][player]["y_sum"] += loc[1]
            positions[team][player]["count"] += 1.0

    result = {}
    for team, players in positions.items():
        result[team] = {}
        for player, data in players.items():
            count = data["count"]
            if count > 0:
                result[team][player] = {
                    "x": data["x_sum"] / count,
                    "y": data["y_sum"] / count,
                    "count": int(count),
                }
    return result


def calculate_passing_connections(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Calculate the top passing connections between players.

    Parameters
    ----------
    events : list[dict]
        Passing events from ``get_passing_events``.

    Returns
    -------
    dict
        {team_name: [{"passer": str, "receiver": str, "count": int}]}
    """
    connections: dict[str, dict[tuple[str, str], int]] = {}
    for e in events:
        team = e.get("team_name")
        passer = e.get("player_name")
        receiver = e.get("receiver_name")
        if team and passer and receiver:
            if team not in connections:
                connections[team] = {}
            pair = (passer, receiver)
            connections[team][pair] = connections[team].get(pair, 0) + 1

    result = {}
    for team, pairs in connections.items():
        sorted_pairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)
        result[team] = [
            {"passer": passer, "receiver": receiver, "count": count}
            for (passer, receiver), count in sorted_pairs
        ]
    return result


def calculate_team_shape(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Estimate tactical team shape metrics: width, depth, compactness, attacking line, defensive line.

    Parameters
    ----------
    events : list[dict]
        Passing events from ``get_passing_events``.

    Returns
    -------
    dict
        {team_name: {"width": float, "depth": float, "compactness": float,
                     "attacking_line": float, "defensive_line": float}}
    """
    avg_pos = calculate_average_positions(events)
    result = {}

    for team, players in avg_pos.items():
        if len(players) < 3:
            result[team] = {
                "width": 0.0,
                "depth": 0.0,
                "compactness": 0.0,
                "attacking_line": 0.0,
                "defensive_line": 0.0,
            }
            continue

        # Sort players by average x coordinate
        sorted_players = sorted(players.items(), key=lambda item: item[1]["x"])
        
        # Assume Goalkeeper has the lowest average x coordinate and exclude them for outfield shape
        outfield = sorted_players[1:] if len(sorted_players) > 3 else sorted_players

        xs = [p[1]["x"] for p in outfield]
        ys = [p[1]["y"] for p in outfield]

        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)

        # Width: max y - min y of outfield players
        width = max(ys) - min(ys)
        # Depth: max x - min x of outfield players
        depth = max(xs) - min(xs)

        # Compactness: average distance to centroid of outfield players
        distances = [math.sqrt((x - mean_x) ** 2 + (y - mean_y) ** 2) for x, y in zip(xs, ys)]
        compactness = sum(distances) / len(distances)

        # Defensive Line: Average x of the 3 deepest outfield players
        def_players = outfield[:min(3, len(outfield))]
        defensive_line = sum(p[1]["x"] for p in def_players) / len(def_players)

        # Attacking Line: Average x of the 3 highest outfield players
        att_players = outfield[-min(3, len(outfield)):]
        attacking_line = sum(p[1]["x"] for p in att_players) / len(att_players)

        result[team] = {
            "width": round(width, 2),
            "depth": round(depth, 2),
            "compactness": round(compactness, 2),
            "attacking_line": round(attacking_line, 2),
            "defensive_line": round(defensive_line, 2),
        }

    return result


def calculate_network_metrics(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Calculate key passing network graph theory metrics.

    Parameters
    ----------
    events : list[dict]
        Passing events from ``get_passing_events``.

    Returns
    -------
    dict
        {team_name: {"most_connected_player": str, "passing_hub": str,
                     "network_density": float, "avg_pass_length": float}}
    """
    team_events: dict[str, list[dict[str, Any]]] = {}
    for e in events:
        team = e.get("team_name")
        if team:
            if team not in team_events:
                team_events[team] = []
            team_events[team].append(e)

    result = {}
    for team, evs in team_events.items():
        players = set()
        pass_counts: dict[str, int] = {}
        receipt_counts: dict[str, int] = {}
        connections: dict[str, set[str]] = {}
        lengths = []

        for e in evs:
            passer = e.get("player_name")
            receiver = e.get("receiver_name")
            start = e.get("location")
            end = e.get("pass_end_location")

            if passer:
                players.add(passer)
                pass_counts[passer] = pass_counts.get(passer, 0) + 1
            if receiver:
                players.add(receiver)
                receipt_counts[receiver] = receipt_counts.get(receiver, 0) + 1
            if passer and receiver:
                if passer not in connections:
                    connections[passer] = set()
                if receiver not in connections:
                    connections[receiver] = set()
                connections[passer].add(receiver)
                connections[receiver].add(passer)
            if start and end:
                dist = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                lengths.append(dist)

        N = len(players)
        if N < 2:
            result[team] = {
                "most_connected_player": "N/A",
                "passing_hub": "N/A",
                "network_density": 0.0,
                "avg_pass_length": 0.0,
            }
            continue

        # Most Connected Player (highest unique connections)
        most_connected = "N/A"
        max_conn = -1
        for p in players:
            conn_count = len(connections.get(p, set()))
            if conn_count > max_conn:
                max_conn = conn_count
                most_connected = p

        # Passing Hub (highest total passes made + received)
        hub = "N/A"
        max_total = -1
        for p in players:
            total = pass_counts.get(p, 0) + receipt_counts.get(p, 0)
            if total > max_total:
                max_total = total
                hub = p

        # Network Density (actual edges / possible edges)
        directed_edges = set()
        for e in evs:
            passer = e.get("player_name")
            receiver = e.get("receiver_name")
            if passer and receiver:
                directed_edges.add((passer, receiver))
        density = len(directed_edges) / (N * (N - 1)) if N > 1 else 0.0

        avg_len = sum(lengths) / len(lengths) if lengths else 0.0

        result[team] = {
            "most_connected_player": most_connected,
            "passing_hub": hub,
            "network_density": round(density, 3),
            "avg_pass_length": round(avg_len, 2),
        }

    return result


def calculate_zone_distribution(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Calculate percentage distribution of passes across the pitch thirds.

    Parameters
    ----------
    events : list[dict]
        Passing events from ``get_passing_events``.

    Returns
    -------
    dict
        {team_name: {"defensive_third": float, "middle_third": float, "final_third": float}}
    """
    result: dict[str, dict[str, int]] = {}
    for e in events:
        team = e.get("team_name")
        loc = e.get("location")
        if team and loc:
            if team not in result:
                result[team] = {"defensive": 0, "middle": 0, "final": 0, "total": 0}
            
            x = loc[0]
            if x < 40:
                result[team]["defensive"] += 1
            elif x < 80:
                result[team]["middle"] += 1
            else:
                result[team]["final"] += 1
            result[team]["total"] += 1

    final_result = {}
    for team, counts in result.items():
        total = counts["total"]
        if total > 0:
            final_result[team] = {
                "defensive_third": round((counts["defensive"] / total) * 100, 1),
                "middle_third": round((counts["middle"] / total) * 100, 1),
                "final_third": round((counts["final"] / total) * 100, 1),
            }
        else:
            final_result[team] = {
                "defensive_third": 0.0,
                "middle_third": 0.0,
                "final_third": 0.0,
            }
    return final_result


def detect_formation(events: list[dict[str, Any]]) -> dict[str, str]:
    """Detect team formation from player average positions.

    Parameters
    ----------
    events : list[dict]
        Passing events from ``get_passing_events``.

    Returns
    -------
    dict
        {team_name: formation_string}
    """
    avg_pos = calculate_average_positions(events)
    result = {}

    for team, players in avg_pos.items():
        if len(players) < 8:
            result[team] = "Unknown"
            continue

        # Sort players by average x coordinate
        sorted_players = sorted(players.items(), key=lambda item: item[1]["x"])
        
        # Exclude GK (lowest average x)
        outfield = sorted_players[1:]
        num_outfield = len(outfield)
        if num_outfield < 5:
            result[team] = "Unknown"
            continue

        xs = [p[1]["x"] for p in outfield]

        # Use maximum gap clustering to find defenders, midfielders, and forwards lines
        best_val = -1
        best_partition = (3, 7)  # default partition (e.g. 4-4-2 size)

        # Iterate over possible defender/midfielder partition indexes
        for i in range(2, 5):  # size of defenders line (usually 3, 4, or 5)
            for j in range(i + 1, num_outfield - 1):
                gap1 = xs[i] - xs[i - 1]
                gap2 = xs[j + 1] - xs[j]
                val = gap1 + gap2

                defenders_count = i
                midfielders_count = j - i + 1
                forwards_count = num_outfield - (j + 1)

                # Check tactical feasibility boundaries
                if (
                    3 <= defenders_count <= 5
                    and 2 <= midfielders_count <= 5
                    and 1 <= forwards_count <= 3
                ):
                    if val > best_val:
                        best_val = val
                        best_partition = (i, j)

        i, j = best_partition
        def_cnt = i
        mid_cnt = j - i + 1
        fwd_cnt = num_outfield - (j + 1)

        # Handle specific formations / sub-variations
        if def_cnt == 4 and mid_cnt == 5 and fwd_cnt == 1:
            mid_xs = xs[i : j + 1]
            # Check if there is a gap indicating 4-2-3-1
            if mid_xs[2] - mid_xs[1] > 5.0:
                formation = "4-2-3-1"
            else:
                formation = "4-3-3"
        elif def_cnt == 4 and mid_cnt == 3 and fwd_cnt == 3:
            formation = "4-3-3"
        elif def_cnt == 3 and mid_cnt == 5 and fwd_cnt == 2:
            formation = "3-5-2"
        elif def_cnt == 4 and mid_cnt == 4 and fwd_cnt == 2:
            formation = "4-4-2"
        elif def_cnt == 5 and mid_cnt == 3 and fwd_cnt == 2:
            formation = "5-3-2"
        elif def_cnt == 5 and mid_cnt == 4 and fwd_cnt == 1:
            formation = "5-4-1"
        else:
            formation = f"{def_cnt}-{mid_cnt}-{fwd_cnt}"

        result[team] = formation

    return result


def calculate_progressive_passes(events: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Filter and return progressive passes for each team.

    Parameters
    ----------
    events : list[dict]
        Passing events from ``get_passing_events``.

    Returns
    -------
    dict
        {team_name: [progressive_pass_events]}
    """
    result: dict[str, list[dict[str, Any]]] = {}
    for e in events:
        team = e.get("team_name")
        start = e.get("location")
        end = e.get("pass_end_location")
        if team and start and end:
            if team not in result:
                result[team] = []

            x_start, y_start = start[0], start[1]
            x_end, y_end = end[0], end[1]

            # Progressive passes must move forward
            if x_end <= x_start:
                continue

            # Distance to opponent's goal center (120, 40)
            dist_start = math.sqrt((x_start - 120) ** 2 + (y_start - 40) ** 2)
            dist_end = math.sqrt((x_end - 120) ** 2 + (y_end - 40) ** 2)

            # Standard progressive threshold definitions (StatsBomb/Opta equivalent in yards)
            if x_start < 60 and x_end < 60:
                threshold = 30.0
            elif x_start < 60 and x_end >= 60:
                threshold = 15.0
            else:
                threshold = 10.0

            if dist_start - dist_end >= threshold:
                result[team].append(e)

    return result
