"""
Type definitions for MLTE integration with Microsoft Agent Framework.

This module provides comprehensive type definitions for agent evaluation,
quality gates, compliance reporting, and evidence management.

Federal Compliance: CMMC L2, NIST 800-171, NIST AI RMF
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional
from enum import Enum
from datetime import datetime


@dataclass
class AgentSpec:
    """
    Specification of an agent for MLTE evaluation.

    This dataclass captures all metadata and configuration needed to
    evaluate an agent's quality, performance, and compliance characteristics.

    Attributes:
        model_id: Unique identifier for the agent model
        version: Semantic version (e.g., "1.0.0")
        name: Human-readable name
        description: Purpose and capabilities description
        instructions: System instructions/prompts
        tools: List of tool/function definitions
        agent_type: Type of agent (ChatAgent, WorkflowAgent, etc.)
        metadata: Additional key-value metadata

    Federal Compliance:
        - Supports NIST AI RMF documentation requirements
        - Enables traceability from requirements to evidence
    """

    model_id: str
    version: str
    name: str
    description: str
    instructions: Optional[str] = None
    tools: List[Dict[str, Any]] = field(default_factory=list)
    agent_type: str = "ChatAgent"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate required fields."""
        if not self.model_id:
            raise ValueError("model_id is required")
        if not self.version:
            raise ValueError("version is required")
        if not self.name:
            raise ValueError("name is required")


@dataclass
class QualityGate:
    """
    Quality gate definition for automated deployment decisions.

    Quality gates define pass/fail criteria for agent evaluation metrics.
    Gates can be blocking (prevent deployment) or non-blocking (warnings).

    Attributes:
        name: Human-readable gate name
        test_case_id: MLTE test case identifier
        threshold: Numeric threshold value
        comparison: Comparison operator (>=, <=, ==, !=, >, <)
        severity: Impact level (critical, high, medium, low)
        blocking: Whether gate failure blocks deployment
        description: Detailed gate description
        metadata: Additional gate configuration

    Example:
        >>> gate = QualityGate(
        ...     name="Minimum Accuracy",
        ...     test_case_id="accuracy",
        ...     threshold=0.95,
        ...     comparison=">=",
        ...     severity="critical",
        ...     blocking=True
        ... )

    Federal Compliance:
        - Maps to CMMC control objectives
        - Supports audit trail requirements
    """

    name: str
    test_case_id: str
    threshold: float
    comparison: Literal[">=", "<=", "==", "!=", ">", "<"]
    severity: Literal["critical", "high", "medium", "low"]
    blocking: bool
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def evaluate(self, value: float) -> bool:
        """
        Evaluate whether a value meets the gate criteria.

        Args:
            value: Measured value to compare against threshold

        Returns:
            True if value meets criteria, False otherwise
        """
        comparisons = {
            ">=": lambda v, t: v >= t,
            "<=": lambda v, t: v <= t,
            "==": lambda v, t: v == t,
            "!=": lambda v, t: v != t,
            ">": lambda v, t: v > t,
            "<": lambda v, t: v < t,
        }
        return comparisons[self.comparison](value, self.threshold)


@dataclass
class GateResult:
    """
    Result of quality gate evaluation.

    Aggregates all gate evaluation results and provides deployment decision.

    Attributes:
        passed: List of gates that passed
        failed: List of gates that failed
        blocking_failures: Subset of failed gates that are blocking
        deployment_allowed: Whether deployment should proceed
        timestamp: When evaluation completed
        metadata: Additional result metadata

    Federal Compliance:
        - Provides evidence for deployment authorization
        - Supports change control documentation
    """

    passed: List[QualityGate] = field(default_factory=list)
    failed: List[QualityGate] = field(default_factory=list)
    blocking_failures: List[QualityGate] = field(default_factory=list)
    deployment_allowed: bool = False
    timestamp: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def pass_rate(self) -> float:
        """Calculate percentage of gates that passed."""
        total = len(self.passed) + len(self.failed)
        return len(self.passed) / total if total > 0 else 0.0

    @property
    def summary(self) -> str:
        """Generate human-readable summary."""
        status = "✅ PASSED" if self.deployment_allowed else "❌ FAILED"
        return f"{status} - {len(self.passed)} passed, {len(self.failed)} failed"


class EvaluationStatus(str, Enum):
    """
    Status of MLTE evaluation workflow.

    Tracks progress through the multi-agent evaluation pipeline.
    """

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class EvaluationReport:
    """
    Complete MLTE evaluation report.

    Aggregates all evaluation artifacts, results, and compliance mappings
    into a comprehensive report suitable for technical and business audiences.

    Attributes:
        agent_spec: Agent being evaluated
        status: Current evaluation status
        negotiation_card_id: MLTE NegotiationCard artifact ID
        test_suite_id: MLTE TestSuite artifact ID
        test_results_id: MLTE TestResults artifact ID
        report_id: MLTE Report artifact ID
        gate_result: Quality gate evaluation results
        compliance_report: Federal compliance mappings
        summary: Human-readable summary
        timestamp: Evaluation start time
        duration_seconds: Total evaluation time
        metadata: Additional report metadata

    Federal Compliance:
        - Complete audit trail from requirements to evidence
        - NIST AI RMF characteristic coverage
        - CMMC control mapping
        - OSCAL-compatible documentation
    """

    agent_spec: AgentSpec
    status: EvaluationStatus
    negotiation_card_id: Optional[str] = None
    test_suite_id: Optional[str] = None
    test_results_id: Optional[str] = None
    report_id: Optional[str] = None
    gate_result: Optional[GateResult] = None
    compliance_report: Optional[Dict[str, Any]] = None
    summary: str = ""
    timestamp: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    duration_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_complete(self) -> bool:
        """Check if evaluation completed successfully."""
        return self.status == EvaluationStatus.COMPLETED

    @property
    def is_passed(self) -> bool:
        """Check if agent passed all quality gates."""
        return (
            self.is_complete
            and self.gate_result is not None
            and self.gate_result.deployment_allowed
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for serialization."""
        return {
            "agent": {
                "model_id": self.agent_spec.model_id,
                "version": self.agent_spec.version,
                "name": self.agent_spec.name,
                "type": self.agent_spec.agent_type,
            },
            "status": self.status.value,
            "artifacts": {
                "negotiation_card_id": self.negotiation_card_id,
                "test_suite_id": self.test_suite_id,
                "test_results_id": self.test_results_id,
                "report_id": self.report_id,
            },
            "gate_result": {
                "passed": len(self.gate_result.passed) if self.gate_result else 0,
                "failed": len(self.gate_result.failed) if self.gate_result else 0,
                "deployment_allowed": self.gate_result.deployment_allowed if self.gate_result else False,
            } if self.gate_result else None,
            "compliance": self.compliance_report,
            "summary": self.summary,
            "timestamp": self.timestamp,
            "duration_seconds": self.duration_seconds,
            "metadata": self.metadata,
        }


@dataclass
class ComplianceReport:
    """
    Federal compliance mapping report.

    Maps agent evaluation results to federal compliance frameworks
    including NIST AI RMF, CMMC, and NIST 800-171.

    Attributes:
        nist_ai_rmf: Mapping of NIST AI RMF characteristics to test case IDs
        cmmc_controls: Mapping of CMMC control IDs to test case IDs
        nist_800_171: Mapping of NIST 800-171 control IDs to test case IDs
        oscal_document: OSCAL-formatted compliance documentation
        gaps: List of compliance gaps identified
        recommendations: Remediation recommendations
        timestamp: Report generation time
        metadata: Additional compliance metadata

    Federal Compliance:
        - NIST AI RMF: All 7 trustworthy characteristics
        - CMMC Level 2: Required practices coverage
        - NIST 800-171: CUI protection requirements
        - OSCAL: Machine-readable compliance documentation

    Example NIST AI RMF Mapping:
        {
            "Valid and Reliable": ["accuracy", "precision_recall"],
            "Safe": ["robustness", "error_handling"],
            "Secure and Resilient": ["prompt_injection", "input_validation"],
            "Accountable and Transparent": ["explainability", "reasoning_trace"],
            "Fair with Harmful Bias Managed": ["fairness", "bias_detection"],
            "Privacy Enhanced": ["data_handling", "pii_protection"],
        }
    """

    nist_ai_rmf: Dict[str, List[str]] = field(default_factory=dict)
    cmmc_controls: Dict[str, List[str]] = field(default_factory=dict)
    nist_800_171: Dict[str, List[str]] = field(default_factory=dict)
    oscal_document: Optional[Dict[str, Any]] = None
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def nist_ai_rmf_coverage(self) -> float:
        """Calculate percentage of NIST AI RMF characteristics covered."""
        total_characteristics = 7  # NIST AI RMF has 7 characteristics
        covered = len([k for k, v in self.nist_ai_rmf.items() if v])
        return covered / total_characteristics

    @property
    def cmmc_coverage(self) -> float:
        """Calculate percentage of CMMC controls covered."""
        if not self.cmmc_controls:
            return 0.0
        total = len(self.cmmc_controls)
        covered = len([k for k, v in self.cmmc_controls.items() if v])
        return covered / total if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert compliance report to dictionary."""
        return {
            "nist_ai_rmf": self.nist_ai_rmf,
            "nist_ai_rmf_coverage": self.nist_ai_rmf_coverage,
            "cmmc_controls": self.cmmc_controls,
            "cmmc_coverage": self.cmmc_coverage,
            "nist_800_171": self.nist_800_171,
            "oscal_document": self.oscal_document,
            "gaps": self.gaps,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class TestInput:
    """
    Test input specification for agent evaluation.

    Encapsulates test input data and expected behavior for measurements.

    Attributes:
        test_case_id: Associated test case identifier
        input_data: Input data for the agent
        expected_output: Expected agent output (optional)
        metadata: Additional test input metadata
    """

    test_case_id: str
    input_data: Any
    expected_output: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MeasurementResult:
    """
    Result of a single measurement execution.

    Attributes:
        test_case_id: Associated test case identifier
        measurement_type: Type of measurement (e.g., "accuracy", "latency")
        value: Measured value
        unit: Unit of measurement (e.g., "ms", "percentage")
        passed: Whether measurement met criteria
        metadata: Additional result metadata
        timestamp: When measurement was taken
    """

    test_case_id: str
    measurement_type: str
    value: float
    unit: str
    passed: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.utcnow().timestamp())


@dataclass
class QASDescriptor:
    """
    Quality Attribute Scenario (QAS) descriptor.

    Describes a quality attribute scenario from MLTE negotiation.

    Attributes:
        quality: Quality attribute (accuracy, security, etc.)
        stimulus: Trigger condition
        source: Input source
        environment: Operational context
        response: Expected behavior
        measure: Quantitative/qualitative measure

    Federal Compliance:
        - Supports requirements traceability per CMMC CA.L2-3.12.4
    """

    quality: str
    stimulus: str
    source: str
    environment: str
    response: str
    measure: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# Type aliases for clarity
EvidenceID = str
TestCaseID = str
ArtifactID = str
ControlID = str

# Constants
NIST_AI_RMF_CHARACTERISTICS = [
    "Valid and Reliable",
    "Safe",
    "Secure and Resilient",
    "Accountable and Transparent",
    "Explainable and Interpretable",
    "Privacy Enhanced",
    "Fair with Harmful Bias Managed",
]

CMMC_LEVEL_2_DOMAINS = [
    "Access Control (AC)",
    "Awareness and Training (AT)",
    "Audit and Accountability (AU)",
    "Configuration Management (CM)",
    "Identification and Authentication (IA)",
    "Incident Response (IR)",
    "Maintenance (MA)",
    "Media Protection (MP)",
    "Personnel Security (PS)",
    "Physical Protection (PE)",
    "Recovery (RE)",
    "Risk Management (RM)",
    "Security Assessment (CA)",
    "Situational Awareness (SA)",
    "System and Communications Protection (SC)",
    "System and Information Integrity (SI)",
]

__all__ = [
    "AgentSpec",
    "QualityGate",
    "GateResult",
    "EvaluationStatus",
    "EvaluationReport",
    "ComplianceReport",
    "TestInput",
    "MeasurementResult",
    "QASDescriptor",
    "EvidenceID",
    "TestCaseID",
    "ArtifactID",
    "ControlID",
    "NIST_AI_RMF_CHARACTERISTICS",
    "CMMC_LEVEL_2_DOMAINS",
]
