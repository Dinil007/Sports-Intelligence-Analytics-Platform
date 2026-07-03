from __future__ import annotations

from typing import Any

from api.utils.serialization import serialize


def _match_events(match_id: int) -> list[dict[str, Any]]:
    from services.match_intelligence_service import get_match_dashboard

    dashboard = get_match_dashboard(match_id)
    return dashboard.get("events", []) if isinstance(dashboard, dict) else []


def player_analytics(match_id: int = 1) -> dict[str, Any]:
    from services import player_intelligence_service

    events = _match_events(match_id)
    return serialize({"statistics": player_intelligence_service.calculate_player_statistics(events), "rankings": player_intelligence_service.calculate_player_rankings(events)})


def team_analytics(match_id: int = 1) -> dict[str, Any]:
    from services import team_intelligence_service

    events = _match_events(match_id)
    return serialize({"kpis": team_intelligence_service.calculate_team_kpis(events), "summary": team_intelligence_service.generate_team_summary(events)})


def match_analytics(match_id: int = 1) -> dict[str, Any]:
    from services.match_intelligence_service import get_match_dashboard

    return serialize(get_match_dashboard(match_id))


def tactical(match_id: int = 1) -> dict[str, Any]:
    from services import tactical_analysis_service
    from services.match_intelligence_service import get_match_dashboard

    return serialize(tactical_analysis_service.generate_full_tactical_analysis(get_match_dashboard(match_id)))


def passing_network(match_id: int = 1) -> dict[str, Any]:
    from services import passing_network_service
    from services.match_intelligence_service import get_match_dashboard

    dashboard = get_match_dashboard(match_id)
    events = passing_network_service.get_passing_events(dashboard)
    return serialize({"average_positions": passing_network_service.calculate_average_positions(events), "connections": passing_network_service.calculate_passing_connections(events), "metrics": passing_network_service.calculate_network_metrics(events)})


def match_momentum(match_id: int = 1) -> dict[str, Any]:
    from services import match_momentum_service

    events = _match_events(match_id)
    return serialize({"momentum": match_momentum_service.calculate_match_momentum(events), "kpis": match_momentum_service.calculate_momentum_kpis(events), "summary": match_momentum_service.generate_match_momentum_summary(events)})


def player_intelligence(match_id: int = 1) -> dict[str, Any]:
    from services import player_intelligence_service

    events = _match_events(match_id)
    return serialize({"scores": player_intelligence_service.calculate_player_scores(events), "radar": player_intelligence_service.calculate_player_radar(events), "summary": player_intelligence_service.generate_player_summary(events)})


def team_intelligence(match_id: int = 1) -> dict[str, Any]:
    return team_analytics(match_id)


def scouting(limit: int = 25) -> dict[str, Any]:
    from services import scouting_service

    players = scouting_service.search_players(limit=limit)
    return serialize({"players": players, "summary": scouting_service.generate_scouting_summary(players)})


def scouting_search(query: str | None = None, limit: int = 25) -> list[dict[str, Any]]:
    from services import scouting_service

    return serialize(scouting_service.search_players(name=query, limit=limit))


def scouting_profile(player_name: str) -> dict[str, Any]:
    from services import scouting_service

    return serialize(scouting_service.get_player_profile(player_name))


def transfer() -> dict[str, Any]:
    from services import transfer_intelligence_service

    return serialize({"targets": transfer_intelligence_service.calculate_transfer_targets(), "budget": transfer_intelligence_service.calculate_transfer_budget(), "summary": transfer_intelligence_service.generate_transfer_summary()})


def transfer_targets() -> list[dict[str, Any]]:
    from services import transfer_intelligence_service

    return serialize(transfer_intelligence_service.calculate_transfer_targets())


def transfer_value() -> list[dict[str, Any]]:
    from services import transfer_intelligence_service

    return serialize(transfer_intelligence_service.calculate_transfer_value())


def athlete_monitoring() -> dict[str, Any]:
    from services import athlete_monitoring_service

    return serialize({
        "training_load": athlete_monitoring_service.calculate_training_load(),
        "workload": athlete_monitoring_service.calculate_workload(),
        "fatigue": athlete_monitoring_service.calculate_fatigue_score(),
        "recovery": athlete_monitoring_service.calculate_recovery_score(),
        "summary": athlete_monitoring_service.generate_athlete_summary(),
    })


def injury_risk() -> dict[str, Any]:
    from services import athlete_monitoring_service

    return serialize({"risk": athlete_monitoring_service.calculate_fatigue_score(), "model_status": "Existing injury-risk endpoint exposed as workload-derived API placeholder where model output is unavailable."})