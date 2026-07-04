"""MLOps constants."""

from __future__ import annotations

# Model stages/states
STAGE_DEVELOPMENT = "Development"
STAGE_TESTING = "Testing"
STAGE_STAGING = "Staging"
STAGE_PRODUCTION = "Production"
STAGE_ARCHIVED = "Archived"
STAGE_ROLLBACK = "Rollback"

VALID_STAGES = {
    STAGE_DEVELOPMENT,
    STAGE_TESTING,
    STAGE_STAGING,
    STAGE_PRODUCTION,
    STAGE_ARCHIVED,
    STAGE_ROLLBACK,
}

# Drift thresholds
DATA_DRIFT_THRESHOLD = 0.05
MODEL_DRIFT_THRESHOLD = 0.08
CONCEPT_DRIFT_THRESHOLD = 0.06
