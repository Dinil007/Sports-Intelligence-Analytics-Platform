"""Unit tests for model training pipelines."""

from __future__ import annotations

import unittest
from prediction.training.train_match_model import train_match_model
from prediction.training.train_player_rating_model import train_player_rating_model
from prediction.training.train_transfer_model import train_transfer_model
from prediction.training.train_injury_model import train_injury_model
from prediction.training.train_market_value_model import train_market_value_model
from prediction.training.train_team_strength_model import train_team_strength_model
from prediction.registry.model_registry import ModelRegistry
from prediction.registry.model_version import ModelVersion
from prediction.utils.serialization import ModelSerializer
from prediction.constants import (
    MODEL_MATCH_OUTCOME,
    MODEL_PLAYER_RATING,
    MODEL_TRANSFER_SUCCESS,
    MODEL_INJURY_RISK,
    MODEL_MARKET_VALUE,
    MODEL_TEAM_STRENGTH,
)


class TestTraining(unittest.TestCase):
    """Verify all training pipelines complete and register correctly."""

    def test_train_match_model(self) -> None:
        version = train_match_model()
        self.assertTrue(ModelVersion.is_valid(version), f"Invalid version: {version}")
        meta = ModelRegistry.get_model_metadata(MODEL_MATCH_OUTCOME)
        self.assertIsNotNone(meta)
        self.assertIn("accuracy", meta["metrics"])
        self.assertGreater(meta["metrics"]["accuracy"], 0.0)

    def test_train_player_rating_model(self) -> None:
        version = train_player_rating_model()
        self.assertTrue(ModelVersion.is_valid(version))
        meta = ModelRegistry.get_model_metadata(MODEL_PLAYER_RATING)
        self.assertIsNotNone(meta)
        self.assertIn("r2_score", meta["metrics"])

    def test_train_transfer_model(self) -> None:
        version = train_transfer_model()
        self.assertTrue(ModelVersion.is_valid(version))
        meta = ModelRegistry.get_model_metadata(MODEL_TRANSFER_SUCCESS)
        self.assertIsNotNone(meta)
        self.assertIn("f1_score", meta["metrics"])

    def test_train_injury_model(self) -> None:
        version = train_injury_model()
        self.assertTrue(ModelVersion.is_valid(version))
        meta = ModelRegistry.get_model_metadata(MODEL_INJURY_RISK)
        self.assertIsNotNone(meta)
        self.assertIn("accuracy", meta["metrics"])

    def test_train_market_value_model(self) -> None:
        version = train_market_value_model()
        self.assertTrue(ModelVersion.is_valid(version))
        meta = ModelRegistry.get_model_metadata(MODEL_MARKET_VALUE)
        self.assertIsNotNone(meta)
        self.assertIn("mae", meta["metrics"])

    def test_train_team_strength_model(self) -> None:
        version = train_team_strength_model()
        self.assertTrue(ModelVersion.is_valid(version))
        meta = ModelRegistry.get_model_metadata(MODEL_TEAM_STRENGTH)
        self.assertIsNotNone(meta)
        self.assertIn("rmse", meta["metrics"])

    def test_serialized_models_exist_on_disk(self) -> None:
        """After training, model files must exist on disk."""
        from prediction.config import config
        for name in [
            MODEL_MATCH_OUTCOME, MODEL_PLAYER_RATING, MODEL_TRANSFER_SUCCESS,
            MODEL_INJURY_RISK, MODEL_MARKET_VALUE, MODEL_TEAM_STRENGTH,
        ]:
            model_file = config.MODELS_DIR / f"{name}.joblib"
            self.assertTrue(model_file.exists(), f"Missing model file: {model_file}")


if __name__ == "__main__":
    unittest.main()
