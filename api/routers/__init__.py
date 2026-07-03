from __future__ import annotations

from fastapi import FastAPI

from api.routers import analytics, athlete_monitoring, health, injury_prediction, match_momentum, matches, passing_network, player_intelligence, players, scouting, tactical, team_intelligence, teams, transfer


def include_routers(app: FastAPI) -> None:
    app.include_router(health.router)
    app.include_router(players.router)
    app.include_router(teams.router)
    app.include_router(matches.router)
    app.include_router(analytics.router)
    app.include_router(tactical.router)
    app.include_router(passing_network.router)
    app.include_router(match_momentum.router)
    app.include_router(player_intelligence.router)
    app.include_router(team_intelligence.router)
    app.include_router(scouting.router)
    app.include_router(transfer.router)
    app.include_router(athlete_monitoring.router)
    app.include_router(injury_prediction.router)