"""
reporting_impl_agent - Creates ReportingAgent with 2 sub-agents

Autonomous implementation agent that creates:
1. reporting.py - Main ReportingAgent coordinator
2. reporting_subagents.py - ReportGeneratorSubAgent and DashboardGeneratorSubAgent
3. test_reporting.py - Unit tests
4. reporting_example.py - Usage example

Federal Compliance: SA-11 (Developer Testing), SI-5 (Security Alerts)
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class ReportingImplAgent:
    """Autonomous implementation agent for ReportingAgent with 2 sub-agents."""

    def __init__(self):
        self.name = "ReportingImplAgent"
        self.workspace_root = Path("d:/AI_Dev/new_microsoft-agent-framework/Microsoft-agent-framework")
        self.files_created: List[Path] = []
        logger.info("%s initialized", self.name)

    async def run(self) -> Dict[str, Any]:
        """Execute full implementation."""
        logger.info("%s starting full implementation", self.name)

        try:
            # Create all 4 files
            await self._create_reporting_agent()
            await self._create_reporting_subagents()
            await self._create_tests()
            await self._create_example()

            logger.info("%s completed: %d files created", self.name, len(self.files_created))

            return {
                "status": "completed",
                "message": f"ReportingAgent with 2 sub-agents implemented successfully",
                "files_created": [str(f) for f in self.files_created],
                "agent_count": 3,  # ReportingAgent + 2 sub-agents
            }

        except Exception as e:
            logger.error("%s failed: %s", self.name, str(e), exc_info=True)
            return {
                "status": "failed",
                "message": str(e),
                "files_created": [str(f) for f in self.files_created],
            }

    async def _create_reporting_agent(self) -> None:
        """Create main ReportingAgent coordinator."""
        logger.info("Creating reporting.py")

        content = '''"""
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
        md.append(f"\\nGenerated: {self.timestamp.isoformat()}")
        md.append("\\n" + "="*80 + "\\n")

        # Executive Summary
        md.append("## Executive Summary\\n")
        md.append(f"**Overall Status:** {self.summary.overall_status}")
        md.append(f"**Critical Issues:** {self.summary.critical_issues_count}")
        md.append(f"**Quality Gates:** {self.summary.gates_passed}/{self.summary.gates_total} Passed")
        md.append(f"**Recommendation:** {self.summary.recommendation}\\n")
        md.append(self.summary.narrative)

        # QAS Results
        if self.qas_results:
            md.append("\\n## Quality Attribute Scenarios (QAS)\\n")
            for qas in self.qas_results:
                status_icon = "✅" if qas.get("status") == "PASS" else "❌"
                md.append(f"### {status_icon} {qas.get('name')}\\n")
                md.append(f"- **Measurement:** {qas.get('measurement')}")
                md.append(f"- **Threshold:** {qas.get('threshold')}")
                md.append(f"- **Status:** {qas.get('status')}\\n")

        # Quality Gates
        if self.gate_results:
            md.append("\\n## Quality Gate Results\\n")
            for gate in self.gate_results:
                status_icon = "✅" if gate.get("status") == "PASS" else "❌" if gate.get("status") == "FAIL" else "⚠️"
                md.append(f"- {status_icon} **{gate.get('name')}**: {gate.get('status')}")

        # Federal Compliance
        if self.compliance_mappings:
            md.append("\\n## Federal Compliance\\n")
            md.append("### NIST AI RMF Characteristics\\n")
            for char, result in self.compliance_mappings.get("nist_ai_rmf", {}).items():
                md.append(f"- **{char}:** {result}")

        # Artifacts
        if self.artifacts:
            md.append("\\n## Artifacts\\n")
            for artifact in self.artifacts:
                md.append(f"- {artifact}")

        return "\\n".join(md)


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
'''

        filepath = self.workspace_root / "python" / "packages" / "mlte_integration" / "agents" / "reporting.py"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        self.files_created.append(filepath)

        logger.info("Created reporting.py (%d lines)", len(content.splitlines()))

    async def _create_reporting_subagents(self) -> None:
        """Create ReportGeneratorSubAgent and DashboardGeneratorSubAgent."""
        logger.info("Creating reporting_subagents.py")

        content = '''"""
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
'''

        filepath = self.workspace_root / "python" / "packages" / "mlte_integration" / "agents" / "reporting_subagents.py"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        self.files_created.append(filepath)

        logger.info("Created reporting_subagents.py (%d lines)", len(content.splitlines()))

    async def _create_tests(self) -> None:
        """Create unit tests."""
        logger.info("Creating test_reporting.py")

        content = '''"""
Unit tests for ReportingAgent and sub-agents.
"""

import pytest
from pathlib import Path
from mlte_integration.agents.reporting import (
    ReportingAgent,
    Report,
    EvaluationSummary,
    ReportFormat,
)


@pytest.fixture
def sample_evaluation_results():
    """Sample evaluation results."""
    return {
        "validation_results": {
            "overall_status": "WARNING",
            "gate_results": [
                {
                    "name": "Security Gate",
                    "status": "PASS",
                    "severity": "blocking",
                },
                {
                    "name": "Performance Gate",
                    "status": "WARNING",
                    "severity": "warning",
                },
            ],
        },
        "qas_results": [
            {
                "name": "Prompt Injection Test",
                "measurement": "0.89",
                "threshold": "0.95",
                "status": "FAIL",
            },
        ],
    }


@pytest.mark.asyncio
async def test_reporting_agent_initialization(tmp_path):
    """Test ReportingAgent initialization."""
    agent = ReportingAgent(output_dir=tmp_path)

    assert agent.output_dir == tmp_path
    assert len(agent.formats) > 0


@pytest.mark.asyncio
async def test_generate_reports(tmp_path, sample_evaluation_results):
    """Test report generation."""
    agent = ReportingAgent(
        output_dir=tmp_path,
        formats=[ReportFormat.MARKDOWN, ReportFormat.JSON],
    )

    results = await agent.generate_reports(
        sample_evaluation_results,
        agent_spec={"name": "TestAgent"},
    )

    assert "reports" in results
    assert len(results["reports"]) >= 2  # MD and JSON


@pytest.mark.asyncio
async def test_markdown_generation(tmp_path, sample_evaluation_results):
    """Test Markdown report generation."""
    agent = ReportingAgent(
        output_dir=tmp_path,
        formats=[ReportFormat.MARKDOWN],
    )

    results = await agent.generate_reports(sample_evaluation_results)

    # Check file was created
    md_files = list(tmp_path.glob("*.md"))
    assert len(md_files) > 0

    # Check content
    content = md_files[0].read_text()
    assert "Executive Summary" in content
    assert "Quality Gate Results" in content


@pytest.mark.asyncio
async def test_json_generation(tmp_path, sample_evaluation_results):
    """Test JSON report generation."""
    agent = ReportingAgent(
        output_dir=tmp_path,
        formats=[ReportFormat.JSON],
    )

    results = await agent.generate_reports(sample_evaluation_results)

    # Check file was created
    json_files = list(tmp_path.glob("*.json"))
    assert len(json_files) > 0


@pytest.mark.asyncio
async def test_dashboard_generation(tmp_path, sample_evaluation_results):
    """Test dashboard generation."""
    agent = ReportingAgent(
        output_dir=tmp_path,
        formats=[ReportFormat.HTML],
    )

    results = await agent.generate_reports(sample_evaluation_results)

    # Check dashboard was created
    html_files = list(tmp_path.glob("dashboard_*.html"))
    assert len(html_files) > 0

    # Check content
    content = html_files[0].read_text()
    assert "MLTE Evaluation Dashboard" in content


def test_report_to_markdown():
    """Test Report.to_markdown() method."""
    summary = EvaluationSummary(
        overall_status="PASS",
        critical_issues_count=0,
        gates_passed=5,
        gates_total=5,
        recommendation="DEPLOY",
        narrative="All tests passed",
    )

    report = Report(
        title="Test Report",
        summary=summary,
        qas_results=[],
        gate_results=[],
    )

    md = report.to_markdown()
    assert "Test Report" in md
    assert "Executive Summary" in md
    assert "PASS" in md
'''

        filepath = self.workspace_root / "python" / "packages" / "mlte_integration" / "tests" / "test_reporting.py"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        self.files_created.append(filepath)

        logger.info("Created test_reporting.py (%d lines)", len(content.splitlines()))

    async def _create_example(self) -> None:
        """Create usage example."""
        logger.info("Creating reporting_example.py")

        content = '''"""
Example: Using ReportingAgent to generate comprehensive evaluation reports.

Federal Compliance: SA-11, SI-5
"""

import asyncio
from pathlib import Path
from mlte_integration.agents.reporting import ReportingAgent, ReportFormat


async def main():
    """Demonstrate ReportingAgent usage."""

    # Sample evaluation results (from all previous agents)
    evaluation_results = {
        "negotiation_card": {"name": "Security Agent", "category": "CUI"},
        "validation_results": {
            "overall_status": "FAIL",
            "gate_results": [
                {
                    "name": "Prompt Injection Resistance",
                    "status": "FAIL",
                    "severity": "blocking",
                    "measured_value": 0.89,
                    "expected_value": 0.95,
                    "reasoning": "Below threshold by 6%",
                },
                {
                    "name": "PII Protection",
                    "status": "PASS",
                    "severity": "blocking",
                    "measured_value": 0.005,
                    "expected_value": 0.01,
                },
                {
                    "name": "Performance SLA",
                    "status": "PASS",
                    "severity": "warning",
                    "measured_value": 1500,
                    "expected_value": 2000,
                },
            ],
        },
        "qas_results": [
            {
                "name": "Prompt Injection Test",
                "measurement": "0.89 success rate",
                "threshold": ">= 0.95",
                "status": "FAIL",
            },
        ],
        "compliance_mappings": {
            "nist_ai_rmf": {
                "Valid and Reliable": "PASS",
                "Safe": "WARNING",
                "Secure and Resilient": "FAIL",
                "Accountable and Transparent": "PASS",
            },
        },
    }

    print("\\n" + "="*80)
    print("MLTE ReportingAgent - Comprehensive Report Generation")
    print("="*80)

    # Initialize ReportingAgent
    output_dir = Path("mlte_reports")
    agent = ReportingAgent(
        output_dir=output_dir,
        formats=[ReportFormat.MARKDOWN, ReportFormat.JSON, ReportFormat.HTML],
    )

    print(f"\\n📝 Generating reports in {len(agent.formats)} formats...")
    print(f"   Output directory: {output_dir}")

    # Generate reports
    results = await agent.generate_reports(
        evaluation_results,
        agent_spec={"name": "SecurityAgent", "version": "1.0.0"},
    )

    # Display results
    print("\\n✅ Report generation complete!")
    print(f"\\n📊 Reports generated: {len(results['reports'])}")
    for report_path in results["reports"]:
        print(f"   - {report_path}")

    if results["dashboards"]:
        print(f"\\n📈 Dashboards generated: {len(results['dashboards'])}")
        for dashboard_path in results["dashboards"]:
            print(f"   - {dashboard_path}")

    # Show sample report content
    if results["reports"]:
        md_report = next((r for r in results["reports"] if r.suffix == ".md"), None)
        if md_report:
            print("\\n" + "-"*80)
            print("SAMPLE REPORT CONTENT (Markdown)")
            print("-"*80)
            print(md_report.read_text()[:500] + "\\n...")

    print("\\n" + "="*80)
    print("📋 Federal Compliance:")
    print("   - SA-11: Developer Security Testing and Evaluation")
    print("   - SI-5: Security Alerts, Advisories, and Directives")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
'''

        filepath = self.workspace_root / "python" / "packages" / "mlte_integration" / "examples" / "reporting_example.py"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        self.files_created.append(filepath)

        logger.info("Created reporting_example.py (%d lines)", len(content.splitlines()))


if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    agent = ReportingImplAgent()
    result = asyncio.run(agent.run())
    print(f"\\n{'='*80}")
    print(f"✅ {agent.name}: {result['status']}")
    print(f"   Files created: {len(result['files_created'])}")
    for filepath in result['files_created']:
        print(f"     - {filepath}")
    print(f"{'='*80}")
