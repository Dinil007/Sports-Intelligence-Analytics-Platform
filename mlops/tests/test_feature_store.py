"""Test MLOps feature store."""

from __future__ import annotations

import unittest
from unittest.mock import patch, MagicMock
from mlops.feature_store.feature_registry import FeatureRegistry
from mlops.feature_store.feature_catalog import FeatureCatalog
from mlops.feature_store.feature_validation import FeatureValidation

class TestFeatureStore(unittest.TestCase):
    """Test suite for feature store operations."""

    @patch("mlops.feature_store.feature_store.FeatureStore.save_store")
    @patch("mlops.feature_store.feature_store.FeatureStore.load_store")
    def test_registry_and_catalog(self, mock_load, mock_save):
        mock_load.return_value = {}
        mock_save.return_value = True

        reg = FeatureRegistry()
        feat = reg.register_feature("goals", "player", "int", "Goals scored")
        self.assertEqual(feat["name"], "goals")
        self.assertEqual(feat["entity"], "player")

    def test_validation(self):
        self.assertTrue(FeatureValidation.validate(5, "int"))
        self.assertTrue(FeatureValidation.validate(5.5, "float"))
        self.assertTrue(FeatureValidation.validate("true", "bool"))
        self.assertFalse(FeatureValidation.validate("abc", "int"))
