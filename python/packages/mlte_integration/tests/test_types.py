"""
Unit tests for MLTE integration type definitions.

Tests validate all dataclasses, enums, and type utilities for correctness,
validation, and federal compliance requirements.

Federal Compliance: Tests ensure types support CMMC L2 audit trail requirements.
"""

import pytest
from datetime import datetime

from agent_framework_mlte_integration.types import (
    AgentSpec,
    QualityGate,
    GateResult,
    EvaluationStatus,
    EvaluationReport,
    ComplianceReport,
    TestInput,
    MeasurementResult,
    QASDescriptor,
    NIST_AI_RMF_CHARACTERISTICS,
    CMMC_LEVEL_2_DOMAINS,
)


class TestAgentSpec:
    """Tests for AgentSpec dataclass."""

    def test_agent_spec_creation(self, sample_agent_spec):
        """Test creating a valid AgentSpec."""
        assert sample_agent_spec.model_id == "test_agent"
        assert sample_agent_spec.version == "1.0.0"
        assert sample_agent_spec.name == "Test Agent"
        assert sample_agent_spec.agent_type == "ChatAgent"
        assert len(sample_agent_spec.tools) == 1
        assert "environment" in sample_agent_spec.metadata

    def test_agent_spec_required_fields(self):
        """Test that required fields are validated."""
        with pytest.raises(ValueError, match="model_id is required"):
            AgentSpec(model_id="", version="1.0.0", name="Test", description="Test")

        with pytest.raises(ValueError, match="version is required"):
            AgentSpec(model_id="test", version="", name="Test", description="Test")

        with pytest.raises(ValueError, match="name is required"):
            AgentSpec(model_id="test", version="1.0.0", name="", description="Test")

    def test_agent_spec_optional_fields(self):
        """Test AgentSpec with minimal required fields."""
        spec = AgentSpec(
            model_id="minimal", version="1.0.0", name="Minimal", description="Test"
        )
        assert spec.instructions is None
        assert spec.tools == []
        assert spec.metadata == {}
        assert spec.agent_type == "ChatAgent"

    def test_agent_spec_with_complex_tools(self):
        """Test AgentSpec with complex tool definitions."""
        spec = AgentSpec(
            model_id="complex",
            version="1.0.0",
            name="Complex Agent",
            description="Complex test agent",
            tools=[
                {
                    "name": "search",
                    "description": "Search tool",
                    "parameters": {"query": "string", "limit": "integer"},
                    "required": ["query"],
                },
                {
                    "name": "calculate",
                    "description": "Calculator tool",
                    "parameters": {"expression": "string"},
                },
            ],
        )
        assert len(spec.tools) == 2
        assert spec.tools[0]["name"] == "search"
        assert "required" in spec.tools[0]


class TestQualityGate:
    """Tests for QualityGate dataclass."""

    def test_quality_gate_creation(self, sample_quality_gate):
        """Test creating a valid QualityGate."""
        assert sample_quality_gate.name == "Minimum Accuracy"
        assert sample_quality_gate.test_case_id == "accuracy"
        assert sample_quality_gate.threshold == 0.95
        assert sample_quality_gate.comparison == ">="
        assert sample_quality_gate.severity == "critical"
        assert sample_quality_gate.blocking is True

    def test_quality_gate_evaluate_greater_equal(self, sample_quality_gate):
        """Test QualityGate evaluation with >= comparison."""
        assert sample_quality_gate.evaluate(0.96) is True
        assert sample_quality_gate.evaluate(0.95) is True
        assert sample_quality_gate.evaluate(0.94) is False

    def test_quality_gate_evaluate_less_equal(self):
        """Test QualityGate evaluation with <= comparison."""
        gate = QualityGate(
            name="Max Latency",
            test_case_id="latency",
            threshold=2000,
            comparison="<=",
            severity="high",
            blocking=False,
        )
        assert gate.evaluate(1500) is True
        assert gate.evaluate(2000) is True
        assert gate.evaluate(2500) is False

    def test_quality_gate_evaluate_equality(self):
        """Test QualityGate evaluation with == comparison."""
        gate = QualityGate(
            name="Exact Match",
            test_case_id="exact",
            threshold=1.0,
            comparison="==",
            severity="medium",
            blocking=False,
        )
        assert gate.evaluate(1.0) is True
        assert gate.evaluate(0.99) is False

    def test_quality_gate_evaluate_all_comparisons(self):
        """Test all comparison operators."""
        test_cases = [
            (">=", 10, 10, True),
            (">=", 11, 10, True),
            (">=", 9, 10, False),
            ("<=", 10, 10, True),
            ("<=", 9, 10, True),
            ("<=", 11, 10, False),
            ("==", 10, 10, True),
            ("==", 9, 10, False),
            ("!=", 9, 10, True),
            ("!=", 10, 10, False),
            (">", 11, 10, True),
            (">", 10, 10, False),
            ("<", 9, 10, True),
            ("<", 10, 10, False),
        ]

        for comparison, value, threshold, expected in test_cases:
            gate = QualityGate(
                name="Test",
                test_case_id="test",
                threshold=threshold,
                comparison=comparison,
                severity="low",
                blocking=False,
            )
            assert gate.evaluate(value) == expected, f"Failed for {comparison}"


class TestGateResult:
    """Tests for GateResult dataclass."""

    def test_gate_result_creation(self):
        """Test creating a GateResult."""
        passed_gate = QualityGate(
            name="Passed",
            test_case_id="pass",
            threshold=0.9,
            comparison=">=",
            severity="high",
            blocking=True,
        )
        failed_gate = QualityGate(
            name="Failed",
            test_case_id="fail",
            threshold=0.95,
            comparison=">=",
            severity="critical",
            blocking=True,
        )

        result = GateResult(
            passed=[passed_gate],
            failed=[failed_gate],
            blocking_failures=[failed_gate],
            deployment_allowed=False,
        )

        assert len(result.passed) == 1
        assert len(result.failed) == 1
        assert len(result.blocking_failures) == 1
        assert result.deployment_allowed is False

    def test_gate_result_pass_rate(self):
        """Test pass_rate property calculation."""
        gate1 = QualityGate(
            "G1", "g1", 0.9, ">=", "high", True
        )
        gate2 = QualityGate("G2", "g2", 0.9, ">=", "high", True)
        gate3 = QualityGate("G3", "g3", 0.9, ">=", "high", True)

        result = GateResult(
            passed=[gate1, gate2], failed=[gate3], blocking_failures=[], deployment_allowed=True
        )

        assert result.pass_rate == pytest.approx(2 / 3)

    def test_gate_result_pass_rate_all_passed(self):
        """Test pass_rate when all gates pass."""
        gate1 = QualityGate("G1", "g1", 0.9, ">=", "high", True)
        gate2 = QualityGate("G2", "g2", 0.9, ">=", "high", True)

        result = GateResult(passed=[gate1, gate2], failed=[], blocking_failures=[], deployment_allowed=True)

        assert result.pass_rate == 1.0

    def test_gate_result_pass_rate_no_gates(self):
        """Test pass_rate with no gates."""
        result = GateResult(passed=[], failed=[], blocking_failures=[], deployment_allowed=True)
        assert result.pass_rate == 0.0

    def test_gate_result_summary(self):
        """Test summary property generation."""
        gate1 = QualityGate("G1", "g1", 0.9, ">=", "high", True)
        gate2 = QualityGate("G2", "g2", 0.9, ">=", "high", True)

        result_passed = GateResult(
            passed=[gate1, gate2], failed=[], blocking_failures=[], deployment_allowed=True
        )
        assert " PASSED" in result_passed.summary
        assert "2 passed, 0 failed" in result_passed.summary

        result_failed = GateResult(
            passed=[gate1], failed=[gate2], blocking_failures=[gate2], deployment_allowed=False
        )
        assert "L FAILED" in result_failed.summary
        assert "1 passed, 1 failed" in result_failed.summary


class TestEvaluationStatus:
    """Tests for EvaluationStatus enum."""

    def test_evaluation_status_values(self):
        """Test all EvaluationStatus enum values."""
        assert EvaluationStatus.NOT_STARTED == "not_started"
        assert EvaluationStatus.IN_PROGRESS == "in_progress"
        assert EvaluationStatus.COMPLETED == "completed"
        assert EvaluationStatus.FAILED == "failed"
        assert EvaluationStatus.CANCELLED == "cancelled"

    def test_evaluation_status_str(self):
        """Test EvaluationStatus string representation."""
        assert str(EvaluationStatus.COMPLETED) == "completed"
        assert str(EvaluationStatus.FAILED) == "failed"


class TestEvaluationReport:
    """Tests for EvaluationReport dataclass."""

    def test_evaluation_report_creation(self, sample_agent_spec):
        """Test creating an EvaluationReport."""
        report = EvaluationReport(
            agent_spec=sample_agent_spec,
            status=EvaluationStatus.COMPLETED,
            negotiation_card_id="card-123",
            test_suite_id="suite-456",
            test_results_id="results-789",
            report_id="report-abc",
            summary="All tests passed",
        )

        assert report.agent_spec.model_id == "test_agent"
        assert report.status == EvaluationStatus.COMPLETED
        assert report.negotiation_card_id == "card-123"
        assert report.summary == "All tests passed"

    def test_evaluation_report_is_complete(self, sample_agent_spec):
        """Test is_complete property."""
        report = EvaluationReport(
            agent_spec=sample_agent_spec, status=EvaluationStatus.COMPLETED
        )
        assert report.is_complete is True

        report_in_progress = EvaluationReport(
            agent_spec=sample_agent_spec, status=EvaluationStatus.IN_PROGRESS
        )
        assert report_in_progress.is_complete is False

    def test_evaluation_report_is_passed(self, sample_agent_spec):
        """Test is_passed property."""
        gate_result = GateResult(
            passed=[], failed=[], blocking_failures=[], deployment_allowed=True
        )

        report = EvaluationReport(
            agent_spec=sample_agent_spec,
            status=EvaluationStatus.COMPLETED,
            gate_result=gate_result,
        )
        assert report.is_passed is True

        report_failed = EvaluationReport(
            agent_spec=sample_agent_spec,
            status=EvaluationStatus.COMPLETED,
            gate_result=GateResult(
                passed=[], failed=[], blocking_failures=[], deployment_allowed=False
            ),
        )
        assert report_failed.is_passed is False

    def test_evaluation_report_to_dict(self, sample_agent_spec):
        """Test to_dict serialization."""
        report = EvaluationReport(
            agent_spec=sample_agent_spec,
            status=EvaluationStatus.COMPLETED,
            negotiation_card_id="card-123",
            summary="Test summary",
            duration_seconds=120.5,
        )

        report_dict = report.to_dict()

        assert report_dict["agent"]["model_id"] == "test_agent"
        assert report_dict["agent"]["version"] == "1.0.0"
        assert report_dict["status"] == "completed"
        assert report_dict["summary"] == "Test summary"
        assert report_dict["duration_seconds"] == 120.5
        assert "artifacts" in report_dict


class TestComplianceReport:
    """Tests for ComplianceReport dataclass."""

    def test_compliance_report_creation(self):
        """Test creating a ComplianceReport."""
        report = ComplianceReport(
            nist_ai_rmf={
                "Valid and Reliable": ["accuracy", "precision"],
                "Safe": ["robustness"],
            },
            cmmc_controls={
                "AC.L2-3.1.1": ["access_control"],
                "IA.L2-3.5.1": ["authentication"],
            },
            gaps=["Privacy Enhanced characteristic not covered"],
        )

        assert len(report.nist_ai_rmf) == 2
        assert len(report.cmmc_controls) == 2
        assert len(report.gaps) == 1

    def test_compliance_report_nist_ai_rmf_coverage(self):
        """Test NIST AI RMF coverage calculation."""
        report = ComplianceReport(
            nist_ai_rmf={
                "Valid and Reliable": ["accuracy"],
                "Safe": ["robustness"],
                "Secure and Resilient": ["security"],
            }
        )

        # 3 out of 7 characteristics covered
        assert report.nist_ai_rmf_coverage == pytest.approx(3 / 7)

    def test_compliance_report_cmmc_coverage(self):
        """Test CMMC coverage calculation."""
        report = ComplianceReport(
            cmmc_controls={
                "AC.L2-3.1.1": ["test1"],
                "IA.L2-3.5.1": ["test2"],
                "AU.L2-3.3.1": [],  # Not covered
            }
        )

        # 2 out of 3 controls covered
        assert report.cmmc_coverage == pytest.approx(2 / 3)

    def test_compliance_report_cmmc_coverage_empty(self):
        """Test CMMC coverage with no controls."""
        report = ComplianceReport(cmmc_controls={})
        assert report.cmmc_coverage == 0.0

    def test_compliance_report_to_dict(self):
        """Test to_dict serialization."""
        report = ComplianceReport(
            nist_ai_rmf={"Valid and Reliable": ["accuracy"]},
            cmmc_controls={"AC.L2-3.1.1": ["access"]},
            gaps=["Gap 1", "Gap 2"],
            recommendations=["Fix Gap 1", "Fix Gap 2"],
        )

        report_dict = report.to_dict()

        assert "nist_ai_rmf" in report_dict
        assert "nist_ai_rmf_coverage" in report_dict
        assert "cmmc_controls" in report_dict
        assert "cmmc_coverage" in report_dict
        assert "gaps" in report_dict
        assert len(report_dict["gaps"]) == 2
        assert len(report_dict["recommendations"]) == 2


class TestTestInput:
    """Tests for TestInput dataclass."""

    def test_test_input_creation(self):
        """Test creating a TestInput."""
        test_input = TestInput(
            test_case_id="test-001",
            input_data={"query": "What is the weather?"},
            expected_output="Sunny, 72F",
            metadata={"category": "weather"},
        )

        assert test_input.test_case_id == "test-001"
        assert test_input.input_data["query"] == "What is the weather?"
        assert test_input.expected_output == "Sunny, 72F"
        assert test_input.metadata["category"] == "weather"

    def test_test_input_without_expected_output(self):
        """Test TestInput without expected output."""
        test_input = TestInput(
            test_case_id="test-002", input_data={"query": "Test"}
        )

        assert test_input.expected_output is None
        assert test_input.metadata == {}


class TestMeasurementResult:
    """Tests for MeasurementResult dataclass."""

    def test_measurement_result_creation(self):
        """Test creating a MeasurementResult."""
        result = MeasurementResult(
            test_case_id="accuracy-001",
            measurement_type="accuracy",
            value=0.96,
            unit="percentage",
            passed=True,
            metadata={"model": "gpt-4"},
        )

        assert result.test_case_id == "accuracy-001"
        assert result.measurement_type == "accuracy"
        assert result.value == 0.96
        assert result.unit == "percentage"
        assert result.passed is True
        assert result.timestamp > 0

    def test_measurement_result_timestamp(self):
        """Test that timestamp is automatically set."""
        result = MeasurementResult(
            test_case_id="test",
            measurement_type="latency",
            value=150.0,
            unit="ms",
            passed=True,
        )

        # Timestamp should be recent (within last minute)
        current_time = datetime.utcnow().timestamp()
        assert abs(result.timestamp - current_time) < 60


class TestQASDescriptor:
    """Tests for QASDescriptor dataclass."""

    def test_qas_descriptor_creation(self):
        """Test creating a QASDescriptor."""
        qas = QASDescriptor(
            quality="accuracy",
            stimulus="User asks a factual question",
            source="User input",
            environment="Production",
            response="Agent provides accurate answer",
            measure="Accuracy >= 95%",
            metadata={"priority": "high"},
        )

        assert qas.quality == "accuracy"
        assert qas.stimulus == "User asks a factual question"
        assert qas.source == "User input"
        assert qas.environment == "Production"
        assert qas.response == "Agent provides accurate answer"
        assert qas.measure == "Accuracy >= 95%"
        assert qas.metadata["priority"] == "high"


class TestConstants:
    """Tests for module constants."""

    def test_nist_ai_rmf_characteristics(self):
        """Test NIST AI RMF characteristics constant."""
        assert len(NIST_AI_RMF_CHARACTERISTICS) == 7
        assert "Valid and Reliable" in NIST_AI_RMF_CHARACTERISTICS
        assert "Safe" in NIST_AI_RMF_CHARACTERISTICS
        assert "Secure and Resilient" in NIST_AI_RMF_CHARACTERISTICS
        assert "Accountable and Transparent" in NIST_AI_RMF_CHARACTERISTICS
        assert "Explainable and Interpretable" in NIST_AI_RMF_CHARACTERISTICS
        assert "Privacy Enhanced" in NIST_AI_RMF_CHARACTERISTICS
        assert "Fair with Harmful Bias Managed" in NIST_AI_RMF_CHARACTERISTICS

    def test_cmmc_level_2_domains(self):
        """Test CMMC Level 2 domains constant."""
        assert len(CMMC_LEVEL_2_DOMAINS) == 16
        assert "Access Control (AC)" in CMMC_LEVEL_2_DOMAINS
        assert "Audit and Accountability (AU)" in CMMC_LEVEL_2_DOMAINS
        assert "Configuration Management (CM)" in CMMC_LEVEL_2_DOMAINS
        assert "Identification and Authentication (IA)" in CMMC_LEVEL_2_DOMAINS
        assert "Security Assessment (CA)" in CMMC_LEVEL_2_DOMAINS
