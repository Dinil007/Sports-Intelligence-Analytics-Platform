from __future__ import annotations

from typing import Any

from api.utils.pagination import PaginationParams, paginate
from api.utils.serialization import serialize


def list_teams(page: int = 1, page_size: int = 25) -> dict[str, Any]:
    from services import player_service

    teams = player_service.get_all_teams() or []
    data = [{"id": index + 1, "name": team} for index, team in enumerate(teams)]
    return paginate(data, PaginationParams(page=page, page_size=page_size))


def get_team(team_id: int | str) -> dict[str, Any]:
    from services import player_service

    teams = player_service.get_all_teams() or []
    if isinstance(team_id, int) or str(team_id).isdigit():
        index = int(team_id) - 1
        if index < 0 or index >= len(teams):
            return {}
        team = teams[index]
    else:
        team = str(team_id)
    return {"id": team_id, "name": team}


def team_rankings(limit: int = 25) -> list[dict[str, Any]]:
    from services import scouting_service

    players = scouting_service.search_players(limit=500)
    by_team: dict[str, list[float]] = {}
    for player in players:
        team = str(player.get("club", "Unknown"))
        by_team.setdefault(team, []).append(float(player.get("sporta_score", 0) or 0))
    rankings = [
        {"team": team, "average_sporta_score": round(sum(scores) / len(scores), 2), "players": len(scores)}
        for team, scores in by_team.items()
        if scores
    ]
    return serialize(sorted(rankings, key=lambda row: row["average_sporta_score"], reverse=True)[:limit])