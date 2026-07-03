"""Formatting of high-level validation metric summaries."""

from __future__ import annotations

from typing import Any, Dict
from prediction.logging import logger

class ModelEvaluationReport:
    """Generates standardized performance reports for model artifacts."""
    
    @staticmethod
    def generate_report(
        model_name: str,
        algorithm: str,
        metrics: Dict[str, float],
        classification: bool = True,
    ) -> str:
        """Create a markdown-formatted evaluation report string."""
        report = []
        report.append(f"# Model Evaluation Report: {model_name}")
        report.append(f"- **Algorithm**: {algorithm}")
        report.append("- **Task Type**: " + ("Classification" if classification else "Regression"))
        report.append("\n## Metrics Summary")
        
        for k, v in metrics.items():
            report.append(f"- **{k.upper()}**: {v:.4f}")
            
        report_str = "\n".join(report)
        logger.info(f"Generated evaluation report for model: {model_name}")
        return report_str
