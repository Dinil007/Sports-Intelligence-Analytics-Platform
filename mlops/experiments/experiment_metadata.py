"""MLOps experiment metadata dataclass."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

@dataclass
class ExperimentMetadata:
    """Represents metadata tracked for a machine learning experiment."""
    experiment_id: str
    model_name: str
    algorithm: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    training_time: float  # in seconds
    dataset: str
    feature_count: int
    model_version: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to dictionary format."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExperimentMetadata:
        """Create metadata from dictionary format."""
        return cls(
            experiment_id=str(data["experiment_id"]),
            model_name=str(data["model_name"]),
            algorithm=str(data["algorithm"]),
            accuracy=float(data["accuracy"]),
            precision=float(data["precision"]),
            recall=float(data["recall"]),
            f1=float(data["f1"]),
            training_time=float(data["training_time"]),
            dataset=str(data["dataset"]),
            feature_count=int(data["feature_count"]),
            model_version=str(data["model_version"]),
            timestamp=str(data["timestamp"])
        )
