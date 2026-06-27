"""Rewrite get_candidate_players() - use vw_scouting directly, drop all unnecessary joins."""
from pathlib import Path

p = Path("database/recommendation_repository.py")
text = p.read_text(encoding="utf-8")

old = '''    base_query = \"\"\"
        SELECT
            s.player_name,
            COALESCE(s.team_name, 'N/A') AS team_name,
            'N/A' AS competition_name,
            b.matches_played,
            COALESCE(sc.sporta_score, 0) AS sporta_score,
            COALESCE(sc.goals, 0) AS goals,
            COALESCE(sc.total_xg, 0) AS total_xg,
            COALESCE(b.passes, 0) AS passes,
            COALESCE(b.dribbles, 0) AS dribbles,
            COALESCE(b.carries, 0) AS carries,
            COALESCE(b.recoveries, 0) AS recoveries,
            COALESCE(b.pressures, 0) AS pressures,
            dp.country_name
        FROM vw_scouting s
        LEFT JOIN mv_player_base_stats b ON s.player_name = b.player_name
        LEFT JOIN vw_sporta_score sc ON s.player_name = sc.player_name
        LEFT JOIN dim_players dp ON s.player_name = dp.player_name
    \"\"\"

    conditions = []
    params: dict = {}

    if club:
        conditions.append(\"s.team_name = :club\")
        params[\"club\"] = club

    if nationality:
        conditions.append(\"dp.country_name = :nationality\")
        params[\"nationality\"] = nationality

    if minutes_played_min is not None:
        conditions.append(\"b.matches_played >= :minutes_played_min\")
        params[\"minutes_played_min\"] = minutes_played_min

    if minutes_played_max is not None:
        conditions.append(\"b.matches_played <= :minutes_played_max\")
        params[\"minutes_played_max\"] = minutes_played_max

    # position, age, competition, season, budget_tier, preferred_foot:
    # accepted for API compatibility but not yet backed by dataset columns.

    if conditions:
        base_query += \" WHERE \" + \" AND \".join(conditions)

    base_query += \" GROUP BY s.player_name, s.team_name, b.matches_played, sc.sporta_score, sc.goals, sc.total_xg, b.passes, b.dribbles, b.carries, b.recoveries, b.pressures, dp.country_name ORDER BY s.player_name;\"'''

new = '''    # vw_scouting already has all stats (sporta_score, goals, total_xg, passes,
    # dribbles, carries, recoveries, pressures).  No further table joins are
    # needed for the core columns; team_name comes from a lightweight subquery
    # only when the club filter is active.
    base_query = \"\"\"
        SELECT
            s.player_name,
            COALESCE(te.team_name, 'N/A') AS team_name,
            'N/A' AS competition_name,
            s.matches_played,
            COALESCE(s.sporta_score, 0) AS sporta_score,
            COALESCE(s.goals, 0) AS goals,
            COALESCE(s.total_xg, 0) AS total_xg,
            COALESCE(s.passes, 0) AS passes,
            COALESCE(s.dribbles, 0) AS dribbles,
            COALESCE(s.carries, 0) AS carries,
            COALESCE(s.recoveries, 0) AS recoveries,
            COALESCE(s.pressures, 0) AS pressures,
            dp.country_name
        FROM vw_scouting s
        LEFT JOIN LATERAL (
            SELECT fme.team_name, COUNT(*) AS cnt
            FROM fact_match_events fme
            WHERE fme.player_name = s.player_name
              AND fme.team_name IS NOT NULL
            GROUP BY fme.team_name
            ORDER BY cnt DESC
            LIMIT 1
        ) te ON TRUE
        LEFT JOIN dim_players dp ON s.player_name = dp.player_name
    \"\"\"

    conditions = []
    params: dict = {}

    if club:
        conditions.append(\"te.team_name = :club\")
        params[\"club\"] = club

    if nationality:
        conditions.append(\"dp.country_name = :nationality\")
        params[\"nationality\"] = nationality

    if minutes_played_min is not None:
        conditions.append(\"s.matches_played >= :minutes_played_min\")
        params[\"minutes_played_min\"] = minutes_played_min

    if minutes_played_max is not None:
        conditions.append(\"s.matches_played <= :minutes_played_max\")
        params[\"minutes_played_max\"] = minutes_played_max

    # position, age, competition, season, budget_tier, preferred_foot:
    # accepted for API compatibility but not yet backed by dataset columns.

    if conditions:
        base_query += \" WHERE \" + \" AND \".join(conditions)

    base_query += \" ORDER BY s.player_name;\"'''

print(f"old found: {old in text}")
if old in text:
    text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")
    print("done")
else:
    print("old not found")
