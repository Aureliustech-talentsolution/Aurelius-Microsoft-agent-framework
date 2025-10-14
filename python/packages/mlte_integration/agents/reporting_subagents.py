"""
ReportingAgent Sub-Agents

1. ReportGeneratorSubAgent - Creates comprehensive reports (MD, JSON, PDF)
2. DashboardGeneratorSubAgent - Creates visual dashboards (HTML)
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import json
import logging

from .reporting import Report, EvaluationSummary, ReportFormat

logger = logging.getLogger(__name__)


class ReportGeneratorSubAgent:
    """
    Generates comprehensive evaluation reports.

    Formats: Markdown, HTML, JSON, PDF
    """

    def __init__(self, output_dir: Path):
        """Initialize report generator."""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("ReportGeneratorSubAgent initialized (output: %s)", output_dir)

    async def generate(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]],
        formats: List[ReportFormat],
    ) -> List[Path]:
        """Generate reports in multiple formats."""
        logger.info("Generating reports in %d formats", len(formats))

        # Create executive summary
        summary = self._create_summary(evaluation_results)

        # Build report object
        report = Report(
            title=f"MLTE Evaluation Report - {agent_spec.get('name', 'Agent') if agent_spec else 'Agent'}",
            summary=summary,
            qas_results=evaluation_results.get("qas_results", []),
            gate_results=evaluation_results.get("gate_results", []),
            compliance_mappings=evaluation_results.get("compliance_mappings"),
            artifacts=self._collect_artifacts(evaluation_results),
        )

        # Generate each format
        generated_files = []
        for fmt in formats:
            filepath = await self._generate_format(report, fmt, agent_spec)
            if filepath:
                generated_files.append(filepath)

        logger.info("Generated %d report files", len(generated_files))
        return generated_files

    def _create_summary(self, evaluation_results: Dict[str, Any]) -> EvaluationSummary:
        """Create executive summary from results."""
        validation_results = evaluation_results.get("validation_results", {})

        overall_status = validation_results.get("overall_status", "UNKNOWN")
        gate_results = validation_results.get("gate_results", [])

        critical_issues = sum(
            1 for g in gate_results
            if g.get("status") == "FAIL" and g.get("severity") == "blocking"
        )

        gates_passed = sum(1 for g in gate_results if g.get("status") == "PASS")
        gates_total = len(gate_results)

        # Determine recommendation
        if overall_status == "FAIL":
            recommendation = "DO_NOT_DEPLOY"
        elif overall_status == "WARNING":
            recommendation = "CONDITIONAL"
        else:
            recommendation = "DEPLOY"

        # Generate narrative
        narrative = self._generate_narrative(
            overall_status, critical_issues, gates_passed, gates_total
        )

        return EvaluationSummary(
            overall_status=overall_status,
            critical_issues_count=critical_issues,
            gates_passed=gates_passed,
            gates_total=gates_total,
            recommendation=recommendation,
            narrative=narrative,
        )

    def _generate_narrative(
        self,
        status: str,
        critical_issues: int,
        gates_passed: int,
        gates_total: int,
    ) -> str:
        """Generate executive summary narrative."""
        if status == "FAIL":
            return (
                f"Agent evaluation FAILED with {critical_issues} critical issue(s). "
                f"Passed {gates_passed}/{gates_total} quality gates. "
                f"The agent must not be deployed to production until all blocking issues are resolved. "
                f"Review detailed findings below for specific remediation guidance."
            )
        elif status == "WARNING":
            return (
                f"Agent evaluation completed with WARNINGS. "
                f"Passed {gates_passed}/{gates_total} quality gates with no blocking failures. "
                f"Some quality gates raised warnings that should be reviewed before deployment. "
                f"Consider addressing warning-level issues to improve agent reliability."
            )
        else:
            return (
                f"Agent evaluation PASSED successfully. "
                f"All {gates_total} quality gates passed. "
                f"The agent meets all quality, security, and compliance requirements. "
                f"Approved for production deployment."
            )

    def _collect_artifacts(self, evaluation_results: Dict[str, Any]) -> List[str]:
        """Collect artifact references."""
        artifacts = []

        # Negotiation card
        if "negotiation_card" in evaluation_results:
            artifacts.append("negotiation_card.json")

        # Test results
        if "test_results" in evaluation_results:
            artifacts.append("test_results.json")

        # Evidence
        if "evidence" in evaluation_results:
            artifacts.append("evidence.json")

        # OSCAL
        if "oscal" in evaluation_results:
            artifacts.append("oscal.json")

        return artifacts

    async def _generate_format(
        self,
        report: Report,
        fmt: ReportFormat,
        agent_spec: Optional[Dict[str, Any]],
    ) -> Optional[Path]:
        """Generate single format."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        agent_name = agent_spec.get("name", "agent") if agent_spec else "agent"

        if fmt == ReportFormat.MARKDOWN:
            filepath = self.output_dir / f"report_{agent_name}_{timestamp}.md"
            content = report.to_markdown()
            filepath.write_text(content, encoding="utf-8")
            logger.info("Generated Markdown report: %s", filepath)
            return filepath

        elif fmt == ReportFormat.JSON:
            filepath = self.output_dir / f"report_{agent_name}_{timestamp}.json"
            content = self._to_json(report)
            filepath.write_text(content, encoding="utf-8")
            logger.info("Generated JSON report: %s", filepath)
            return filepath

        elif fmt == ReportFormat.HTML:
            filepath = self.output_dir / f"report_{agent_name}_{timestamp}.html"
            content = self._to_html(report)
            filepath.write_text(content, encoding="utf-8")
            logger.info("Generated HTML report: %s", filepath)
            return filepath

        elif fmt == ReportFormat.PDF:
            # PDF generation requires additional dependencies (e.g., reportlab)
            # For now, generate Markdown and log note about PDF conversion
            logger.warning("PDF generation not yet implemented, generating Markdown instead")
            return await self._generate_format(report, ReportFormat.MARKDOWN, agent_spec)

        return None

    def _to_json(self, report: Report) -> str:
        """Convert report to JSON."""
        data = {
            "title": report.title,
            "timestamp": report.timestamp.isoformat(),
            "summary": {
                "overall_status": report.summary.overall_status,
                "critical_issues": report.summary.critical_issues_count,
                "gates_passed": report.summary.gates_passed,
                "gates_total": report.summary.gates_total,
                "recommendation": report.summary.recommendation,
                "narrative": report.summary.narrative,
            },
            "qas_results": report.qas_results,
            "gate_results": report.gate_results,
            "compliance_mappings": report.compliance_mappings,
            "artifacts": report.artifacts,
        }
        return json.dumps(data, indent=2)

    def _to_html(self, report: Report) -> str:
        """Convert report to HTML."""
        # Simple HTML template
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{report.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .warning {{ color: orange; }}
    </style>
</head>
<body>
    <h1>{report.title}</h1>
    <p><em>Generated: {report.timestamp.isoformat()}</em></p>

    <div class="summary">
        <h2>Executive Summary</h2>
        <p><strong>Overall Status:</strong> <span class="{report.summary.overall_status.lower()}">{report.summary.overall_status}</span></p>
        <p><strong>Critical Issues:</strong> {report.summary.critical_issues_count}</p>
        <p><strong>Quality Gates:</strong> {report.summary.gates_passed}/{report.summary.gates_total} Passed</p>
        <p><strong>Recommendation:</strong> {report.summary.recommendation}</p>
        <p>{report.summary.narrative}</p>
    </div>

    <h2>Quality Gate Results</h2>
    <ul>
"""
        for gate in report.gate_results:
            status_class = gate.get("status", "").lower()
            html += f'<li class="{status_class}"><strong>{gate.get("name")}</strong>: {gate.get("status")}</li>'

        html += """
    </ul>
</body>
</html>
"""
        return html


class DashboardGeneratorSubAgent:
    """
    Generates visual dashboards.

    Creates interactive HTML dashboards with charts and metrics.
    """

    def __init__(self, output_dir: Path):
        """Initialize dashboard generator."""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("DashboardGeneratorSubAgent initialized (output: %s)", output_dir)

    async def generate(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]],
    ) -> List[Path]:
        """Generate interactive dashboard."""
        logger.info("Generating visual dashboard")

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        agent_name = agent_spec.get("name", "agent") if agent_spec else "agent"
        filepath = self.output_dir / f"dashboard_{agent_name}_{timestamp}.html"

        # Create dashboard HTML
        html = self._create_dashboard_html(evaluation_results, agent_spec)
        filepath.write_text(html, encoding="utf-8")

        logger.info("Generated dashboard: %s", filepath)
        return [filepath]

    def _create_dashboard_html(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]],
    ) -> str:
        """Create dashboard HTML with embedded charts."""
        agent_name = agent_spec.get("name", "Agent") if agent_spec else "Agent"

        validation_results = evaluation_results.get("validation_results", {})
        gate_results = validation_results.get("gate_results", [])

        passed = sum(1 for g in gate_results if g.get("status") == "PASS")
        failed = sum(1 for g in gate_results if g.get("status") == "FAIL")
        warnings = sum(1 for g in gate_results if g.get("status") == "WARNING")

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>MLTE Dashboard - {agent_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f0f0f0;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .metric-value {{ font-size: 48px; font-weight: bold; margin: 10px 0; }}
        .metric-label {{ color: #666; font-size: 14px; text-transform: uppercase; }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .chart {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 MLTE Evaluation Dashboard</h1>
            <h2>{agent_name}</h2>
            <p><em>Generated: {datetime.utcnow().isoformat()}</em></p>
        </div>

        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Overall Status</div>
                <div class="metric-value {validation_results.get('overall_status', '').lower()}">{validation_results.get('overall_status', 'UNKNOWN')}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Passed</div>
                <div class="metric-value pass">{passed}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Failed</div>
                <div class="metric-value fail">{failed}</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">Warnings</div>
                <div class="metric-value warning">{warnings}</div>
            </div>
        </div>

        <div class="chart">
            <h3>Quality Gate Results</h3>
            <ul>
"""

        for gate in gate_results:
            status = gate.get("status", "UNKNOWN")
            status_class = status.lower()
            html += f'<li class="{status_class}"><strong>{gate.get("name")}</strong>: {status}</li>'

        html += """
            </ul>
        </div>
    </div>
</body>
</html>
"""
        return html
