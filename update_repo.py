path = 'd:/Sports Intelligence & Analytics Platform/database/recommendation_repository.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old1 = '''    base_query = """
        SELECT
            s.player_name,
            COALESCE(te.team_name, 'N/A') AS team_name,
            COALESCE(dc.competition_name, 'N/A') AS competition_name,
            b.matches_played,
            COALESCE(sc.sporta_score, 0) AS sporta_score,
            COALESCE(sc.goals, 0) AS goals,
            COALESCE(sc.total_xg, 0) AS total_xg,
            b.passes,
            b.dribbles,
            b.carries,
            b.recoveries,
            b.pressures
        FROM vw_scouting s
        LEFT JOIN mv_player_base_stats b ON s.player_name = b.player_name
        LEFT JOIN vw_sporta_score sc ON s.player_name = sc.player_name
        LEFT JOIN fact_match_events fme ON s.player_name = fme.player_name
        LEFT JOIN fact_matches fm ON fme.match_id = fm.match_id
        LEFT JOIN dim_competitions dc ON fm.competition_id = dc.competition_id
        LEFT JOIN dim_seasons ds ON fm.season_id = ds.season_id
        LEFT JOIN dim_teams te ON fme.team_name = te.team_name
        LEFT JOIN dim_players dp ON s.player_name = dp.player_name
    """'''

new1 = '''    base_query = """
        SELECT
            s.player_name,
            COALESCE(te.team_name, 'N/A') AS team_name,
            COALESCE(dc.competition_name, 'N/A') AS competition_name,
            b.matches_played,
            COALESCE(sc.sporta_score, 0) AS sporta_score,
            COALESCE(sc.goals, 0) AS goals,
            COALESCE(sc.total_xg, 0) AS total_xg,
            b.passes,
            b.dribbles,
            b.carries,
            b.recoveries,
            b.pressures,
            dp.country_name
        FROM vw_scouting s
        LEFT JOIN mv_player_base_stats b ON s.player_name = b.player_name
        LEFT JOIN vw_sporta_score sc ON s.player_name = sc.player_name
        LEFT JOIN fact_match_events fme ON s.player_name = fme.player_name
        LEFT JOIN fact_matches fm ON fme.match_id = fm.match_id
        LEFT JOIN dim_competitions dc ON fm.competition_id = dc.competition_id
        LEFT JOIN dim_seasons ds ON fm.season_id = ds.season_id
        LEFT JOIN dim_teams te ON fme.team_name = te.team_name
        LEFT JOIN dim_players dp ON s.player_name = dp.player_name
    """'''

old2 = '''    base_query += " GROUP BY s.player_name, te.team_name, dc.competition_name, b.matches_played, sc.sporta_score, sc.goals, sc.total_xg, b.passes, b.dribbles, b.carries, b.recoveries, b.pressures ORDER BY s.player_name;"'''

new2 = '''    base_query += " GROUP BY s.player_name, te.team_name, dc.competition_name, b.matches_played, sc.sporta_score, sc.goals, sc.total_xg, b.passes, b.dribbles, b.carries, b.recoveries, b.pressures, dp.country_name ORDER BY s.player_name;"'''

old3 = '''        results.append({
            "player_name": row[0],
            "team_name": row[1],
            "competition_name": row[2],
            "matches_played": row[3],
            "sporta_score": row[4],
            "goals": row[5],
            "total_xg": row[6],
            "passes": row[7],
            "dribbles": row[8],
            "carries": row[9],
            "recoveries": row[10],
            "pressures": row[11],
        })'''

new3 = '''        results.append({
            "player_name": row[0],
            "team_name": row[1],
            "club": row[1],
            "competition_name": row[2],
            "matches_played": row[3],
            "minutes_played": row[3],
            "sporta_score": row[4],
            "goals": row[5],
            "total_xg": row[6],
            "assists": None,
            "pass_accuracy": None,
            "passes": row[7],
            "dribbles": row[8],
            "carries": row[9],
            "recoveries": row[10],
            "pressures": row[11],
            "progressive_passes": None,
            "nationality": row[12],
            "position": None,
            "age": None,
            "preferred_foot": None,
        })'''

for old, new in [(old1, new1), (old2, new2), (old3, new3)]:
    if old not in content:
        print(f'NOT FOUND: {old[:80]}')
    else:
        content = content.replace(old, new)
        print('REPLACED')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Repository updated')
