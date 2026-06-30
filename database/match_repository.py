"""
database/match_repository.py
================================
Data-access layer for Match Intelligence.

All SQL for match-related data lives here.
No Streamlit. No Plotly. No ML. No business logic.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import text

from database.db_connection import engine


def _get_conn():
    return engine.connect()


def fetch_matches():
    """Return all matches with home/away team names."""
    sql = text("""
        SELECT
            m.match_id,
            m.match_date,
            m.kick_off,
            c.competition_name,
            s.season_name,
            ht.team_name   AS home_team,
            at.team_name   AS away_team,
            m.home_score,
            m.away_score
        FROM fact_matches m
        JOIN dim_competitions c ON m.competition_id = c.competition_id
        JOIN dim_seasons s      ON m.season_id = s.season_id
        JOIN dim_teams ht       ON m.home_team_id = ht.team_id
        JOIN dim_teams at       ON m.away_team_id = at.team_id
        ORDER BY m.match_date DESC
    """)
    with _get_conn() as conn:
        rows = conn.execute(sql).mappings().fetchall()
    return [dict(r) for r in rows]


def fetch_match(match_id: int):
    """Return a single match record with team names, or None."""
    sql = text("""
        SELECT
            m.match_id,
            m.match_date,
            m.kick_off,
            c.competition_name,
            s.season_name,
            ht.team_name   AS home_team,
            at.team_name   AS away_team,
            m.home_score,
            m.away_score
        FROM fact_matches m
        JOIN dim_competitions c ON m.competition_id = c.competition_id
        JOIN dim_seasons s      ON m.season_id = s.season_id
        JOIN dim_teams ht       ON m.home_team_id = ht.team_id
        JOIN dim_teams at       ON m.away_team_id = at.team_id
        WHERE m.match_id = :mid
        LIMIT 1
    """)
    with _get_conn() as conn:
        row = conn.execute(sql, {"mid": match_id}).mappings().fetchone()
    return dict(row) if row else None


def fetch_match_events(match_id: int):
    """Return all events for a match (raw event stream)."""
    sql = text("""
        SELECT
            id,
            match_id,
            minute,
            second,
            period,
            event_type,
            player_id,
            player_name,
            team_id,
            team_name,
            possession,
            play_pattern,
            CASE
                WHEN location_x IS NOT NULL AND location_y IS NOT NULL
                THEN ARRAY[location_x, location_y]
                ELSE NULL
            END AS location,
            CASE
                WHEN pass_end_x IS NOT NULL AND pass_end_y IS NOT NULL
                THEN ARRAY[pass_end_x, pass_end_y]
                ELSE NULL
            END AS pass_end_location,
            CASE
                WHEN carry_end_x IS NOT NULL AND carry_end_y IS NOT NULL
                THEN ARRAY[carry_end_x, carry_end_y]
                ELSE NULL
            END AS carry_end_location,
            CASE
                WHEN shot_end_x IS NOT NULL
                THEN
                    CASE
                        WHEN shot_end_z IS NOT NULL
                        THEN ARRAY[shot_end_x, shot_end_y, shot_end_z]
                        ELSE ARRAY[shot_end_x, shot_end_y]
                    END
                ELSE NULL
            END AS shot_end_location,
            CASE
                WHEN pressure_x IS NOT NULL AND pressure_y IS NOT NULL
                THEN ARRAY[pressure_x, pressure_y]
                ELSE NULL
            END AS pressure_location,
            CASE
                WHEN block_x IS NOT NULL AND block_y IS NOT NULL
                THEN ARRAY[block_x, block_y]
                ELSE NULL
            END AS block_location,
            CASE
                WHEN interception_x IS NOT NULL AND interception_y IS NOT NULL
                THEN ARRAY[interception_x, interception_y]
                ELSE NULL
            END AS interception_location,
            CASE
                WHEN clearance_x IS NOT NULL AND clearance_y IS NOT NULL
                THEN ARRAY[clearance_x, clearance_y]
                ELSE NULL
            END AS clearance_location,
            CASE
                WHEN ball_receipt_x IS NOT NULL AND ball_receipt_y IS NOT NULL
                THEN ARRAY[ball_receipt_x, ball_receipt_y]
                ELSE NULL
            END AS ball_receipt_location
        FROM fact_match_events
        WHERE match_id = :mid
        ORDER BY minute ASC, second ASC
    """)
    with _get_conn() as conn:
        rows = conn.execute(sql, {"mid": match_id}).mappings().fetchall()
    return [dict(r) for r in rows]


def fetch_match_players(match_id: int):
    """Return distinct players who appeared in a match."""
    sql = text("""
        SELECT DISTINCT
            p.player_id,
            p.player_name,
            p.nickname,
            p.jersey_number,
            p.country_name
        FROM dim_players p
        JOIN fact_match_events e ON e.player_id = p.player_id
        WHERE e.match_id = :mid
        ORDER BY p.jersey_number
    """)
    with _get_conn() as conn:
        rows = conn.execute(sql, {"mid": match_id}).mappings().fetchall()
    return [dict(r) for r in rows]


def fetch_match_lineups(match_id: int):
    """Return a dict with keys 'home' / 'away', each a list of player dicts."""
    match = fetch_match(match_id)
    if not match:
        return {"home": [], "away": []}

    home_team = match["home_team"]
    away_team = match["away_team"]

    sq = text("""
        SELECT DISTINCT ON (e.player_id)
            e.player_id,
            e.player_name,
            e.team_name,
            p.nickname,
            p.jersey_number,
            p.country_name
        FROM fact_match_events e
        LEFT JOIN dim_players p ON e.player_id = p.player_id
        WHERE e.match_id = :mid
          AND e.player_id IS NOT NULL
        ORDER BY e.player_id, e.minute ASC
    """)
    with _get_conn() as conn:
        rows = conn.execute(sq, {"mid": match_id}).mappings().fetchall()

    home_players = []
    away_players = []
    for row in rows:
        entry = {
            "player_id": row["player_id"],
            "player_name": row["player_name"],
            "nickname": row["nickname"],
            "jersey_number": row["jersey_number"],
            "country_name": row["country_name"],
        }
        if row["team_name"] == home_team:
            home_players.append(entry)
        elif row["team_name"] == away_team:
            away_players.append(entry)

    return {"home": home_players, "away": away_players}


def fetch_team_statistics(match_id: int):
    """Return per-team aggregate stats derived from match events."""
    events = fetch_match_events(match_id)
    if not events:
        return {}

    teams = sorted({e["team_name"] for e in events if e.get("team_name")})
    if len(teams) < 2:
        return {}

    home_team = teams[0]
    away_team = teams[1]

    def team_events(name):
        return [e for e in events if e.get("team_name") == name]

    def _count(evs, etype):
        return sum(1 for e in evs if e.get("event_type") == etype)

    def _avg_possession(evs):
        vals = [e["possession"] for e in evs if e.get("possession") is not None]
        if not vals:
            return None
        return sum(vals) / len(vals)

    home = team_events(home_team)
    away = team_events(away_team)

    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_events": len(home),
        "away_events": len(away),
        "home_possession_avg": _avg_possession(home),
        "away_possession_avg": _avg_possession(away),
        "home_passes": _count(home, "Pass"),
        "away_passes": _count(away, "Pass"),
        "home_shots": _count(home, "Shot"),
        "away_shots": _count(away, "Shot"),
        "home_pressures": _count(home, "Pressure"),
        "away_pressures": _count(away, "Pressure"),
        "home_carries": _count(home, "Carry"),
        "away_carries": _count(away, "Carry"),
        "home_dribbles": _count(home, "Dribble"),
        "away_dribbles": _count(away, "Dribble"),
        "home_recoveries": _count(home, "Ball Recovery"),
        "away_recoveries": _count(away, "Ball Recovery"),
        "home_fouls_committed": _count(home, "Foul Committed"),
        "away_fouls_committed": _count(away, "Foul Committed"),
        "home_fouls_won": _count(home, "Foul Won"),
        "away_fouls_won": _count(away, "Foul Won"),
    }


def fetch_player_statistics(match_id: int):
    """Return per-player aggregate stats for a match."""
    events = fetch_match_events(match_id)
    if not events:
        return []

    from collections import defaultdict
    buckets = defaultdict(lambda: {
        "player_id": None,
        "player_name": "Unknown",
        "team_name": None,
        "minutes_played": 0,
        "events": 0,
        "passes": 0,
        "shots": 0,
        "carries": 0,
        "dribbles": 0,
        "pressures": 0,
        "recoveries": 0,
        "fouls_committed": 0,
        "fouls_won": 0,
    })

    for e in events:
        pid = e.get("player_id")
        if pid is None:
            continue
        if buckets[pid]["player_id"] is None:
            buckets[pid]["player_id"] = pid
            buckets[pid]["player_name"] = e.get("player_name", "Unknown")
            buckets[pid]["team_name"] = e.get("team_name")
        b = buckets[pid]
        b["events"] += 1
        et = e.get("event_type", "")
        if et == "Pass":
            b["passes"] += 1
        elif et == "Shot":
            b["shots"] += 1
        elif et == "Carry":
            b["carries"] += 1
        elif et == "Dribble":
            b["dribbles"] += 1
        elif et == "Pressure":
            b["pressures"] += 1
        elif et == "Ball Recovery":
            b["recoveries"] += 1
        elif et == "Foul Committed":
            b["fouls_committed"] += 1
        elif et == "Foul Won":
            b["fouls_won"] += 1
        minute = e.get("minute") or 0
        if minute > b["minutes_played"]:
            b["minutes_played"] = minute

    sorted_players = sorted(buckets.values(), key=lambda p: p["events"], reverse=True)
    return sorted_players
