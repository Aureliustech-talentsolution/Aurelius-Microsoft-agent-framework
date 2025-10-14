"""
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
