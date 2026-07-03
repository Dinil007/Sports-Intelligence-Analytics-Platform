from __future__ import annotations

from typing import Any

from api.utils.pagination import PaginationParams, paginate
from api.utils.serialization import serialize


def list_players(page: int = 1, page_size: int = 25) -> dict[str, Any]:
    from services import player_service

    names = player_service.get_filtered_players() or []
    data = [{"id": index + 1, "name": name} for index, name in enumerate(names)]
    return paginate(serialize(data), PaginationParams(page=page, page_size=page_size))


def get_player(player_id: int | str) -> dict[str, Any]:
    from services import player_service

    if isinstance(player_id, int) or str(player_id).isdigit():
        names = player_service.get_filtered_players() or []
        index = int(player_id) - 1
        if index < 0 or index >= len(names):
            return {}
        player_id = names[index]
    return serialize(player_service.get_player_profile(str(player_id)) or {})


def search_players(query: str | None = None, limit: int = 25) -> list[dict[str, Any]]:
    from services import player_service

    names = player_service.get_filtered_players() or []
    if query:
        names = [name for name in names if query.lower() in str(name).lower()]
    return [{"id": index + 1, "name": name} for index, name in enumerate(names[:limit])]


def top_players(limit: int = 25) -> list[dict[str, Any]]:
    from services import scouting_service

    players = scouting_service.search_players(limit=max(limit, 1))
    return serialize(sorted(players, key=lambda row: row.get("sporta_score", 0), reverse=True)[:limit])