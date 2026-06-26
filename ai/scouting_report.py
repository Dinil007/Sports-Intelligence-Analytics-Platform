import pandas as pd
import numpy as np

def _safe_float(value) -> float:
    """Safely convert a value to float, returning 0.0 if conversion fails."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def generate_scouting_report(player1_stats: pd.Series, player2_stats: pd.Series) -> dict:
    """
    Generates a structured scouting report comparing two players based on their statistics.

    Parameters:
    -----------
    player1_stats : pd.Series
        A Series containing statistics for Player 1.
    player2_stats : pd.Series
        A Series containing statistics for Player 2.

    Returns:
    --------
    dict
        A dictionary containing the structured scouting report.
    """

    report = {
        "best_attacker": "Insufficient data",
        "best_creator": "Insufficient data",
        "best_ball_carrier": "Insufficient data",
        "best_defender": "Insufficient data",
        "strengths_player1": [],
        "strengths_player2": [],
        "weaknesses_player1": [],
        "weaknesses_player2": [],
        "tactical_recommendation": "Insufficient data",
        "overall_verdict": "Insufficient data",
    }

    p1_name = player1_stats.get("player_name", "Player 1")
    p2_name = player2_stats.get("player_name", "Player 2")

    # 1. Best Attacker
    goals_p1 = _safe_float(player1_stats.get("goals"))
    goals_p2 = _safe_float(player2_stats.get("goals"))
    shots_p1 = _safe_float(player1_stats.get("shots"))
    shots_p2 = _safe_float(player2_stats.get("shots"))
    xg_p1 = _safe_float(player1_stats.get("total_xg"))
    xg_p2 = _safe_float(player2_stats.get("total_xg"))

    attack_score_p1 = goals_p1 * 0.4 + shots_p1 * 0.2 + xg_p1 * 0.4
    attack_score_p2 = goals_p2 * 0.4 + shots_p2 * 0.2 + xg_p2 * 0.4

    if attack_score_p1 > attack_score_p2:
        report["best_attacker"] = p1_name
    elif attack_score_p2 > attack_score_p1:
        report["best_attacker"] = p2_name
    elif attack_score_p1 > 0: # If scores are equal but non-zero
        report["best_attacker"] = f"Both {p1_name} and {p2_name} are strong attackers"
    else:
        report["best_attacker"] = "Insufficient data or comparable attacking output"


    # 2. Best Creator
    assists_p1 = _safe_float(player1_stats.get("assists"))
    assists_p2 = _safe_float(player2_stats.get("assists"))
    key_passes_p1 = _safe_float(player1_stats.get("key_passes"))
    key_passes_p2 = _safe_float(player2_stats.get("key_passes"))
    passes_p1 = _safe_float(player1_stats.get("passes"))
    passes_p2 = _safe_float(player2_stats.get("passes"))

    creator_score_p1 = assists_p1 * 0.5 + key_passes_p1 * 0.3 + passes_p1 * 0.2
    creator_score_p2 = assists_p2 * 0.5 + key_passes_p2 * 0.3 + passes_p2 * 0.2

    if creator_score_p1 > creator_score_p2:
        report["best_creator"] = p1_name
    elif creator_score_p2 > creator_score_p1:
        report["best_creator"] = p2_name
    elif creator_score_p1 > 0:
        report["best_creator"] = f"Both {p1_name} and {p2_name} show good creativity"
    else:
        report["best_creator"] = "Insufficient data or comparable creative output"

    # 3. Best Ball Carrier
    dribbles_p1 = _safe_float(player1_stats.get("dribbles"))
    dribbles_p2 = _safe_float(player2_stats.get("dribbles"))
    carries_p1 = _safe_float(player1_stats.get("carries"))
    carries_p2 = _safe_float(player2_stats.get("carries"))

    carrier_score_p1 = dribbles_p1 * 0.6 + carries_p1 * 0.4
    carrier_score_p2 = dribbles_p2 * 0.6 + carries_p2 * 0.4

    if carrier_score_p1 > carrier_score_p2:
        report["best_ball_carrier"] = p1_name
    elif carrier_score_p2 > carrier_score_p1:
        report["best_ball_carrier"] = p2_name
    elif carrier_score_p1 > 0:
        report["best_ball_carrier"] = f"Both {p1_name} and {p2_name} are good ball carriers"
    else:
        report["best_ball_carrier"] = "Insufficient data or comparable ball-carrying ability"

    # 4. Best Defender
    recoveries_p1 = _safe_float(player1_stats.get("recoveries"))
    recoveries_p2 = _safe_float(player2_stats.get("recoveries"))
    pressures_p1 = _safe_float(player1_stats.get("pressures"))
    pressures_p2 = _safe_float(player2_stats.get("pressures"))
    tackles_p1 = _safe_float(player1_stats.get("tackles"))
    tackles_p2 = _safe_float(player2_stats.get("tackles"))
    interceptions_p1 = _safe_float(player1_stats.get("interceptions"))
    interceptions_p2 = _safe_float(player2_stats.get("interceptions"))

    defender_score_p1 = recoveries_p1 * 0.3 + pressures_p1 * 0.3 + tackles_p1 * 0.2 + interceptions_p1 * 0.2
    defender_score_p2 = recoveries_p2 * 0.3 + pressures_p2 * 0.3 + tackles_p2 * 0.2 + interceptions_p2 * 0.2

    if defender_score_p1 > defender_score_p2:
        report["best_defender"] = p1_name
    elif defender_score_p2 > defender_score_p1:
        report["best_defender"] = p2_name
    elif defender_score_p1 > 0:
        report["best_defender"] = f"Both {p1_name} and {p2_name} contribute defensively"
    else:
        report["best_defender"] = "Insufficient data or comparable defensive output"

    # 5. Key Strengths and Weaknesses
    def analyze_strengths_weaknesses(player_stats: pd.Series, player_name: str):
        strengths = []
        weaknesses = []

        # Offensive metrics
        if _safe_float(player_stats.get("goals")) > 0.5 * RADAR_BENCHMARKS.get("goals", 1):
            strengths.append("Strong goal threat")
        elif _safe_float(player_stats.get("goals")) == 0:
            weaknesses.append("Limited goal threat")

        if _safe_float(player_stats.get("total_xg")) > 0.5 * RADAR_BENCHMARKS.get("total_xg", 1):
            strengths.append("High expected goals (xG) production")
        elif _safe_float(player_stats.get("total_xg")) == 0:
            weaknesses.append("Low xG production")

        if _safe_float(player_stats.get("shots")) > 0.5 * RADAR_BENCHMARKS.get("shots", 1):
            strengths.append("High shot volume")
        elif _safe_float(player_stats.get("shots")) == 0:
            weaknesses.append("Low shot volume")

        # Passing/Creativity metrics
        if _safe_float(player_stats.get("passes")) > 0.5 * RADAR_BENCHMARKS.get("passes", 1):
            strengths.append("Excellent passing volume")
        elif _safe_float(player_stats.get("passes")) == 0:
            weaknesses.append("Low passing volume")

        if _safe_float(player_stats.get("assists")) > 0.5 * RADAR_BENCHMARKS.get("assists", 1) or \
           _safe_float(player_stats.get("key_passes")) > 0.5 * RADAR_BENCHMARKS.get("key_passes", 1):
            strengths.append("Strong creative play and assists")
        elif _safe_float(player_stats.get("assists")) == 0 and _safe_float(player_stats.get("key_passes")) == 0:
            weaknesses.append("Limited creative output")

        # Ball carrying metrics
        if _safe_float(player_stats.get("dribbles")) > 0.5 * RADAR_BENCHMARKS.get("dribbles", 1):
            strengths.append("Effective dribbler")
        elif _safe_float(player_stats.get("dribbles")) == 0:
            weaknesses.append("Low dribble volume")

        if _safe_float(player_stats.get("carries")) > 0.5 * RADAR_BENCHMARKS.get("carries", 1):
            strengths.append("Good ball progression through carries")
        elif _safe_float(player_stats.get("carries")) == 0:
            weaknesses.append("Minimal progressive carries")

        # Defensive metrics
        if _safe_float(player_stats.get("recoveries")) > 0.5 * RADAR_BENCHMARKS.get("recoveries", 1):
            strengths.append("Strong in ball recoveries")
        elif _safe_float(player_stats.get("recoveries")) == 0:
            weaknesses.append("Low ball recovery rate")

        if _safe_float(player_stats.get("pressures")) > 0.5 * RADAR_BENCHMARKS.get("pressures", 1):
            strengths.append("High pressing intensity")
        elif _safe_float(player_stats.get("pressures")) == 0:
            weaknesses.append("Limited defensive pressure")

        if _safe_float(player_stats.get("tackles")) > 0.5 * RADAR_BENCHMARKS.get("tackles", 1):
            strengths.append("Effective tackler")
        elif _safe_float(player_stats.get("tackles")) == 0:
            weaknesses.append("Low tackle success")

        if _safe_float(player_stats.get("interceptions")) > 0.5 * RADAR_BENCHMARKS.get("interceptions", 1):
            strengths.append("Good positional awareness for interceptions")
        elif _safe_float(player_stats.get("interceptions")) == 0:
            weaknesses.append("Few interceptions")

        return strengths, weaknesses

    # Using a simplified benchmark value for dynamic analysis as RADAR_BENCHMARKS is in chart_service.py.
    # For a more robust solution, these benchmarks should ideally be accessible or redefined here.
    # For now, I'm making a reasonable assumption or using a simplified approach.
    from services.chart_service import RADAR_BENCHMARKS
    
    strengths1, weaknesses1 = analyze_strengths_weaknesses(player1_stats, p1_name)
    strengths2, weaknesses2 = analyze_strengths_weaknesses(player2_stats, p2_name)

    report["strengths_player1"] = strengths1
    report["strengths_player2"] = strengths2
    report["weaknesses_player1"] = weaknesses1
    report["weaknesses_player2"] = weaknesses2

    # 7. Tactical Recommendation and 8. Overall Verdict
    # This part can be greatly enhanced with an LLM. For now, a rule-based approach.

    if attack_score_p1 > attack_score_p2 and creator_score_p1 > creator_score_p2:
        report["tactical_recommendation"] = f"{p1_name} is better suited for an attacking role, potentially as a forward or an advanced playmaker. {p2_name} might be better in a supporting or defensive role."
        report["overall_verdict"] = f"{p1_name} demonstrates superior offensive and creative capabilities, making them the more impactful player in the final third. {p2_name} provides a more balanced contribution."
    elif attack_score_p2 > attack_score_p1 and creator_score_p2 > creator_score_p1:
        report["tactical_recommendation"] = f"{p2_name} is better suited for an attacking role, potentially as a forward or an advanced playmaker. {p1_name} might be better in a supporting or defensive role."
        report["overall_verdict"] = f"{p2_name} demonstrates superior offensive and creative capabilities, making them the more impactful player in the final third. {p1_name} provides a more balanced contribution."
    elif defender_score_p1 > defender_score_p2 and carrier_score_p1 > carrier_score_p2:
        report["tactical_recommendation"] = f"{p1_name} excels in defensive duties and ball progression, making them ideal for a holding midfield or defensive full-back role. {p2_name} could be used in a more advanced position."
        report["overall_verdict"] = f"{p1_name} offers significant defensive stability and effective ball carrying, crucial for breaking opposition lines. {p2_name} is more focused on attacking aspects."
    elif defender_score_p2 > defender_score_p1 and carrier_score_p2 > carrier_score_p1:
        report["tactical_recommendation"] = f"{p2_name} excels in defensive duties and ball progression, making them ideal for a holding midfield or defensive full-back role. {p1_name} could be used in a more advanced position."
        report["overall_verdict"] = f"{p2_name} offers significant defensive stability and effective ball carrying, crucial for breaking opposition lines. {p1_name} is more focused on attacking aspects."
    else:
        report["tactical_recommendation"] = f"Both players offer a balanced profile. {p1_name} might edge out in some areas while {p2_name} in others. Their utilization would depend on specific team tactics."
        report["overall_verdict"] = f"The players show comparable performance across several key metrics. A detailed tactical analysis is required to determine the best fit for a specific team strategy."

    # Fallback for empty strengths/weaknesses if data is truly insufficient
    if not report["strengths_player1"] and not report["weaknesses_player1"]:
        report["strengths_player1"].append("Data for this player is limited.")
    if not report["strengths_player2"] and not report["weaknesses_player2"]:
        report["strengths_player2"].append("Data for this player is limited.")

    return report
