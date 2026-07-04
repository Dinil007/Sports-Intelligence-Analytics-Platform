"""Test MLOps model registry."""

from __future__ import annotations

import unittest
from unittest.mock import patch, MagicMock
from mlops.registry.model_lifecycle import ModelLifecycle
from mlops.registry.version_manager import VersionManager

class TestRegistry(unittest.TestCase):
    """Test suite for model lifecycle and versions."""

    @patch("mlops.registry.production_registry.ProductionRegistry.save_registry")
    @patch("mlops.registry.production_registry.ProductionRegistry.load_registry")
    def test_lifecycle(self, mock_load, mock_save):
        mock_load.return_value = {}
        mock_save.return_value = True

        lifecycle = ModelLifecycle()
        model = lifecycle.register("test_id", "Test Model", "1.0.0", "Desc")
        
        self.assertEqual(model["model_id"], "test_id")
        self.assertEqual(model["stage"], "Development")

    def test_version_validation(self):
        self.assertTrue(VersionManager.is_valid_version("1.0.0"))
        self.assertFalse(VersionManager.is_valid_version("1.0"))
        self.assertEqual(VersionManager.increment_patch("1.0.0"), "1.0.1")
