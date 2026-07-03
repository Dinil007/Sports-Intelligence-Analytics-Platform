"""Unit and integration tests for validation, enrichment, and pipeline processing."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone
from streaming.pipeline.event_validator import EventValidator
from streaming.pipeline.event_transformer import EventTransformer
from streaming.pipeline.event_enrichment import EventEnricher
from streaming.pipeline.event_loader import EventLoader
from streaming.pipeline.pipeline_manager import PipelineManager
from streaming.monitoring.pipeline_health import register_monitored_pipeline, get_pipeline_health
from streaming.monitoring.stream_metrics import calculate_stream_throughput, calculate_processing_latency, calculate_error_rate

class TestPipeline(unittest.TestCase):
    """Verify validation, transformation, enrichment, and monitoring routines."""
    
    def setUp(self) -> None:
        EventLoader.clear_database()
        self.manager = PipelineManager("test-pipeline")
        self.manager.start_pipeline()
        register_monitored_pipeline(self.manager)

    def test_validation_success(self) -> None:
        event = {
            "event_id": "evt-v1",
            "timestamp": "2026-07-03T12:00:00Z",
            "event_type": "PASS",
            "player_id": 1,
            "team_id": 1,
            "coordinates": [50.0, 50.0],
        }
        is_valid, err = EventValidator.validate_event(event)
        self.assertTrue(is_valid)
        self.assertIsNone(err)

    def test_validation_failure_coordinates(self) -> None:
        event = {
            "event_id": "evt-v2",
            "timestamp": "2026-07-03T12:00:00Z",
            "event_type": "PASS",
            "coordinates": [150.0, 50.0],  # Out of bounds
        }
        is_valid, err = EventValidator.validate_event(event)
        self.assertFalse(is_valid)
        self.assertIn("Coordinates out of bounds", err)

    def test_transformation(self) -> None:
        legacy_event = {
            "id": "evt-t1",
            "timestamp": "2026-07-03T12:00:00Z",
            "action": "shot",
            "x_coord": 88.5,
            "y_coord": 45.2,
        }
        transformed = EventTransformer.transform(legacy_event)
        self.assertEqual(transformed["event_id"], "evt-t1")
        self.assertEqual(transformed["event_type"], "SHOT")
        self.assertEqual(transformed["coordinates"], (88.5, 45.2))

    def test_enrichment(self) -> None:
        event = {
            "event_id": "evt-e1",
            "timestamp": "2026-07-03T12:00:00Z",
            "event_type": "PASS",
            "player_id": 1,
            "team_id": 1,
        }
        enriched = EventEnricher.enrich(event)
        self.assertEqual(enriched["player_name"], "Lionel Andrés Messi Cuccittini")
        self.assertEqual(enriched["team_name"], "Barcelona")
        self.assertEqual(enriched["competition"], "La Liga")

    def test_full_pipeline_ingestion(self) -> None:
        event = {
            "event_id": "evt-p1",
            "timestamp": "2026-07-03T12:00:00Z",
            "event_type": "PASS",
            "player_id": 1,
            "team_id": 1,
            "coordinates": [50.0, 50.0],
            "match_id": 101,
        }
        success = self.manager.ingest_event(event)
        self.assertTrue(success)
        
        # Verify it was loaded
        loaded = EventLoader.get_persisted_events()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["event_id"], "evt-p1")
        self.assertEqual(loaded[0]["player_name"], "Lionel Andrés Messi Cuccittini")
        
        # Check metrics
        self.assertEqual(self.manager.processed_count, 1)
        self.assertEqual(self.manager.error_count, 0)
        self.assertEqual(get_pipeline_health("test-pipeline"), "HEALTHY")
        self.assertEqual(calculate_error_rate("test-pipeline"), 0.0)
        self.assertGreater(calculate_processing_latency("test-pipeline"), 0.0)

    def tearDown(self) -> None:
        self.manager.stop_pipeline()
        EventLoader.clear_database()

if __name__ == "__main__":
    unittest.main()
