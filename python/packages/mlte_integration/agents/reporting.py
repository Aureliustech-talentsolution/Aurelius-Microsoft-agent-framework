"""
ReportingAgent - Comprehensive Evaluation Reporting Coordinator

Coordinates report generation using 2 sub-agents:
1. ReportGeneratorSubAgent - Creates comprehensive reports (MD, JSON, PDF)
2. DashboardGeneratorSubAgent - Creates visual dashboards

Federal Compliance: SA-11 (Developer Testing), SI-5 (Security Alerts)
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ReportFormat(Enum):
    """Supported report formats."""
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    PDF = "pdf"


@dataclass
class EvaluationSummary:
    """Executive summary of evaluation results."""
    overall_status: str  # PASS, FAIL, WARNING
    critical_issues_count: int
    gates_passed: int
    gates_total: int
    recommendation: str  # deploy, do_not_deploy, conditional
    narrative: str  # 2-3 paragraph summary


@dataclass
class Report:
    """Comprehensive evaluation report."""
    title: str
    summary: EvaluationSummary
    qas_results: List[Dict[str, Any]]
    gate_results: List[Dict[str, Any]]
    compliance_mappings: Optional[Dict[str, Any]] = None
    artifacts: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    format: ReportFormat = ReportFormat.MARKDOWN

    def to_markdown(self) -> str:
        """Convert report to Markdown format."""
        md = []

        # Header
        md.append(f"# {self.title}")
        md.append(f"\nGenerated: {self.timestamp.isoformat()}")
        md.append("\n" + "="*80 + "\n")

        # Executive Summary
        md.append("## Executive Summary\n")
        md.append(f"**Overall Status:** {self.summary.overall_status}")
        md.append(f"**Critical Issues:** {self.summary.critical_issues_count}")
        md.append(f"**Quality Gates:** {self.summary.gates_passed}/{self.summary.gates_total} Passed")
        md.append(f"**Recommendation:** {self.summary.recommendation}\n")
        md.append(self.summary.narrative)

        # QAS Results
        if self.qas_results:
            md.append("\n## Quality Attribute Scenarios (QAS)\n")
            for qas in self.qas_results:
                status_icon = "✅" if qas.get("status") == "PASS" else "❌"
                md.append(f"### {status_icon} {qas.get('name')}\n")
                md.append(f"- **Measurement:** {qas.get('measurement')}")
                md.append(f"- **Threshold:** {qas.get('threshold')}")
                md.append(f"- **Status:** {qas.get('status')}\n")

        # Quality Gates
        if self.gate_results:
            md.append("\n## Quality Gate Results\n")
            for gate in self.gate_results:
                status_icon = "✅" if gate.get("status") == "PASS" else "❌" if gate.get("status") == "FAIL" else "⚠️"
                md.append(f"- {status_icon} **{gate.get('name')}**: {gate.get('status')}")

        # Federal Compliance
        if self.compliance_mappings:
            md.append("\n## Federal Compliance\n")
            md.append("### NIST AI RMF Characteristics\n")
            for char, result in self.compliance_mappings.get("nist_ai_rmf", {}).items():
                md.append(f"- **{char}:** {result}")

        # Artifacts
        if self.artifacts:
            md.append("\n## Artifacts\n")
            for artifact in self.artifacts:
                md.append(f"- {artifact}")

        return "\n".join(md)


class ReportingAgent:
    """
    Coordinates comprehensive evaluation reporting.

    Architecture:
        ReportingAgent (Coordinator)
        ├→ ReportGeneratorSubAgent: Creates comprehensive reports
        └→ DashboardGeneratorSubAgent: Creates visual dashboards

    Federal Compliance:
        - SA-11: Developer Security Testing and Evaluation
        - SI-5: Security Alerts, Advisories, and Directives
    """

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        formats: Optional[List[ReportFormat]] = None,
    ):
        """Initialize ReportingAgent."""
        self.output_dir = output_dir or Path("mlte_reports")
        self.formats = formats or [ReportFormat.MARKDOWN, ReportFormat.JSON]
        self.report_generator = None  # Lazy init
        self.dashboard_generator = None  # Lazy init

        logger.info("ReportingAgent initialized (output: %s, formats: %d)",
                   self.output_dir, len(self.formats))

    async def generate_reports(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[Path]]:
        """
        Generate comprehensive evaluation reports in multiple formats.

        Args:
            evaluation_results: Complete evaluation results from all agents
            agent_spec: Optional agent specification

        Returns:
            Dict mapping format to list of generated file paths
        """
        logger.info("Starting report generation in %d formats", len(self.formats))

        # Lazy import sub-agents
        if self.report_generator is None:
            from .reporting_subagents import ReportGeneratorSubAgent, DashboardGeneratorSubAgent
            self.report_generator = ReportGeneratorSubAgent(self.output_dir)
            self.dashboard_generator = DashboardGeneratorSubAgent(self.output_dir)

        # Phase 1: Generate comprehensive reports
        reports = await self.report_generator.generate(
            evaluation_results,
            agent_spec,
            formats=self.formats,
        )

        # Phase 2: Generate visual dashboards (if HTML format requested)
        dashboards = []
        if ReportFormat.HTML in self.formats:
            dashboards = await self.dashboard_generator.generate(
                evaluation_results,
                agent_spec,
            )

        # Organize results by format
        results = {
            "reports": reports,
            "dashboards": dashboards,
        }

        logger.info("Report generation complete: %d reports, %d dashboards",
                   len(reports), len(dashboards))

        return results


# Federal Compliance Annotations
ReportingAgent.__annotations__["federal_compliance"] = {
    "SA-11": "Developer Security Testing and Evaluation - Comprehensive test reporting",
    "SI-5": "Security Alerts, Advisories, and Directives - Security finding communication",
}
