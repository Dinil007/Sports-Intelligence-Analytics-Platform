"""Unit tests for all inference prediction functions."""

from __future__ import annotations

import unittest
from prediction.inference.predict_match import predict_match
from prediction.inference.predict_player_rating import predict_player_rating
from prediction.inference.predict_transfer_success import predict_transfer_success
from prediction.inference.predict_injury_risk import predict_injury_risk
from prediction.inference.predict_market_value import predict_market_value
from prediction.inference.predict_team_strength import predict_team_strength


class TestPrediction(unittest.TestCase):
    """Verify all inference functions return structurally correct results."""

    def test_predict_match(self) -> None:
        features = {
            "home_goals_avg": 2.1,
            "away_goals_avg": 1.2,
            "home_shots_avg": 14.5,
            "away_shots_avg": 9.8,
            "home_possession_avg": 58.0,
            "away_possession_avg": 42.0,
            "home_win_rate": 0.65,
            "away_win_rate": 0.40,
            "goal_difference": 2.0,
        }
        result = predict_match(features)
        self.assertIn("prediction", result)
        self.assertIn(result["prediction"], ["Home Win", "Draw", "Away Win"])
        self.assertIn("confidence", result)
        self.assertGreater(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

    def test_predict_player_rating(self) -> None:
        features = {
            "goals": 2.0,
            "assists": 1.0,
            "passes_completed": 55.0,
            "pass_completion_rate": 0.88,
            "shots_on_target": 3.0,
            "tackles_won": 2.0,
            "interceptions": 1.0,
            "key_passes": 4.0,
            "dribbles_completed": 3.0,
            "minutes_played": 90.0,
        }
        result = predict_player_rating(features)
        self.assertIn("predicted_rating", result)
        self.assertGreaterEqual(result["predicted_rating"], 5.0)
        self.assertLessEqual(result["predicted_rating"], 10.0)

    def test_predict_transfer_success(self) -> None:
        features = {
            "player_age": 24.0,
            "market_value": 25_000_000.0,
            "goals_per_season": 15.0,
            "assists_per_season": 8.0,
            "minutes_played": 2800.0,
            "league_level": 1.0,
            "transfer_fee": 30_000_000.0,
            "destination_league_level": 1.0,
            "fitness_score": 90.0,
        }
        result = predict_transfer_success(features)
        self.assertIn("prediction", result)
        self.assertIn(result["prediction"], ["Successful", "Unsuccessful"])
        self.assertGreater(result["probability"], 0.0)

    def test_predict_injury_risk(self) -> None:
        features = {
            "age": 32.0,
            "minutes_played_last_30": 540.0,
            "fatigue_score": 88.0,
            "sprint_count": 160.0,
            "previous_injuries": 4.0,
            "training_load": 92.0,
            "bmi": 23.5,
            "matches_last_30_days": 9.0,
            "recovery_days": 1.0,
        }
        result = predict_injury_risk(features)
        self.assertIn("risk_level", result)
        self.assertIn(result["risk_level"], ["Low", "Medium", "High"])
        self.assertGreater(result["confidence"], 0.0)

    def test_predict_market_value(self) -> None:
        features = {
            "age": 25.0,
            "goals_per_season": 20.0,
            "assists_per_season": 12.0,
            "sporta_score": 88.0,
            "international_caps": 35.0,
            "league_level": 1.0,
            "years_contract_remaining": 3.0,
            "pass_completion_rate": 0.87,
            "goals_per_90": 0.65,
        }
        result = predict_market_value(features)
        self.assertIn("estimated_value_eur", result)
        self.assertIn("estimated_value_m", result)
        self.assertGreater(result["estimated_value_eur"], 0.0)

    def test_predict_team_strength(self) -> None:
        features = {
            "avg_player_rating": 7.4,
            "goals_scored_season": 72.0,
            "goals_conceded_season": 28.0,
            "possession_avg": 58.0,
            "pass_completion_avg": 0.88,
            "xg_for": 2.1,
            "xg_against": 0.9,
            "win_rate": 0.72,
            "clean_sheet_rate": 0.42,
            "squad_depth_score": 85.0,
        }
        result = predict_team_strength(features)
        self.assertIn("team_strength_score", result)
        self.assertGreaterEqual(result["team_strength_score"], 10.0)
        self.assertLessEqual(result["team_strength_score"], 100.0)


if __name__ == "__main__":
    unittest.main()
