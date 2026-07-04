"""MLOps deployment manager module."""

from __future__ import annotations

from typing import Any
from mlops.constants import STAGE_PRODUCTION, STAGE_ROLLBACK
from mlops.registry.deployment_registry import DeploymentRegistry
from mlops.deployment.stage_manager import StageManager
from mlops.deployment.production_manager import ProductionManager
from mlops.deployment.rollback_manager import RollbackManager

class DeploymentManager:
    """Orchestrates model lifecycle transitions and deployments."""

    def __init__(self) -> None:
        self.registry = DeploymentRegistry()
        self.stage_mgr = StageManager()
        self.prod_mgr = ProductionManager()
        self.rollback_mgr = RollbackManager()

    def deploy(self, model_id: str, version: str, stage: str) -> dict[str, Any]:
        """Deploy model version to targeted stage."""
        if stage == STAGE_PRODUCTION:
            res = self.prod_mgr.promote_to_production(model_id, version)
        else:
            res = self.stage_mgr.transition_stage(model_id, version, stage)
            
        status = "Success" if res else "Failed"
        self.registry.log_deployment(model_id, version, stage, status)
        return {"model_id": model_id, "version": version, "stage": stage, "status": status}

    def rollback(self, model_id: str, rollback_version: str) -> dict[str, Any]:
        """Rollback production model deployment to stable prior version."""
        res = self.rollback_mgr.execute_rollback(model_id, rollback_version)
        status = "Success" if res else "Failed"
        self.registry.log_deployment(model_id, rollback_version, STAGE_ROLLBACK, status)
        return {"model_id": model_id, "version": rollback_version, "stage": STAGE_ROLLBACK, "status": status}
