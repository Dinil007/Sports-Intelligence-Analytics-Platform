"""Unit tests for the Model Registry and Version tracking."""

from __future__ import annotations

import unittest
import json
from prediction.registry.model_registry import ModelRegistry
from prediction.registry.model_version import ModelVersion
from prediction.config import config


class TestModelVersion(unittest.TestCase):
    """Verify version string formatting and increment logic."""

    def test_initial_version(self) -> None:
        self.assertEqual(ModelVersion.initial(), "v1")

    def test_is_valid(self) -> None:
        self.assertTrue(ModelVersion.is_valid("v1"))
        self.assertTrue(ModelVersion.is_valid("v10"))
        self.assertFalse(ModelVersion.is_valid("1"))
        self.assertFalse(ModelVersion.is_valid("version1"))
        self.assertFalse(ModelVersion.is_valid(""))

    def test_increment(self) -> None:
        self.assertEqual(ModelVersion.increment("v1"), "v2")
        self.assertEqual(ModelVersion.increment("v5"), "v6")
        self.assertEqual(ModelVersion.increment("v99"), "v100")

    def test_increment_invalid_returns_v1(self) -> None:
        self.assertEqual(ModelVersion.increment("invalid"), "v1")


class TestModelRegistry(unittest.TestCase):
    """Verify model registry CRUD operations."""

    TEST_MODEL = "test_dummy_model"

    def setUp(self) -> None:
        """Clear any existing test model entries before each test."""
        if config.REGISTRY_PATH.exists():
            with open(config.REGISTRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.pop(self.TEST_MODEL, None)
            with open(config.REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

    def test_register_first_version(self) -> None:
        version = ModelRegistry.register_model(
            model_name=self.TEST_MODEL,
            algorithm="RandomForest",
            metrics={"accuracy": 0.89, "f1_score": 0.87},
            location="/prediction/serialized_models/test_dummy_model.joblib",
            status="candidate",
        )
        self.assertEqual(version, "v1")

    def test_register_increments_version(self) -> None:
        ModelRegistry.register_model(
            model_name=self.TEST_MODEL,
            algorithm="RandomForest",
            metrics={"accuracy": 0.89},
            location="/prediction/serialized_models/test_dummy_model.joblib",
            status="candidate",
        )
        version2 = ModelRegistry.register_model(
            model_name=self.TEST_MODEL,
            algorithm="XGBoost",
            metrics={"accuracy": 0.91},
            location="/prediction/serialized_models/test_dummy_model_v2.joblib",
            status="production",
        )
        self.assertEqual(version2, "v2")

    def test_get_model_metadata_latest(self) -> None:
        ModelRegistry.register_model(
            model_name=self.TEST_MODEL,
            algorithm="LogisticRegression",
            metrics={"accuracy": 0.82},
            location="/prediction/serialized_models/test_dummy_model.joblib",
        )
        meta = ModelRegistry.get_model_metadata(self.TEST_MODEL)
        self.assertIsNotNone(meta)
        self.assertEqual(meta["algorithm"], "LogisticRegression")
        self.assertIn("accuracy", meta["metrics"])

    def test_get_model_metadata_specific_version(self) -> None:
        ModelRegistry.register_model(
            model_name=self.TEST_MODEL,
            algorithm="GradientBoosting",
            metrics={"accuracy": 0.85},
            location="/prediction/serialized_models/test_dummy_model.joblib",
        )
        ModelRegistry.register_model(
            model_name=self.TEST_MODEL,
            algorithm="XGBoost",
            metrics={"accuracy": 0.90},
            location="/prediction/serialized_models/test_dummy_model_v2.joblib",
        )
        meta_v1 = ModelRegistry.get_model_metadata(self.TEST_MODEL, version="v1")
        self.assertEqual(meta_v1["algorithm"], "GradientBoosting")

    def test_update_status(self) -> None:
        ModelRegistry.register_model(
            model_name=self.TEST_MODEL,
            algorithm="XGBoost",
            metrics={"accuracy": 0.90},
            location="/prediction/serialized_models/test_dummy_model.joblib",
            status="candidate",
        )
        updated = ModelRegistry.update_status(self.TEST_MODEL, "v1", "production")
        self.assertTrue(updated)
        meta = ModelRegistry.get_model_metadata(self.TEST_MODEL, version="v1")
        self.assertEqual(meta["status"], "production")

    def test_get_nonexistent_model_returns_none(self) -> None:
        meta = ModelRegistry.get_model_metadata("does_not_exist_xyz")
        self.assertIsNone(meta)

    def tearDown(self) -> None:
        """Clean up test model entries after each test."""
        if config.REGISTRY_PATH.exists():
            with open(config.REGISTRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.pop(self.TEST_MODEL, None)
            with open(config.REGISTRY_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)


if __name__ == "__main__":
    unittest.main()
