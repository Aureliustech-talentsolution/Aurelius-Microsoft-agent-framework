"""
MLTE Integration for Microsoft Agent Framework.

This package provides seamless integration between the Microsoft Agent Framework
and MLTE (Machine Learning Test and Evaluation), enabling automated, evidence-based
quality assurance for AI agents with federal compliance support.

Key Components:
- MLTEOrchestratorAgent: Main orchestrator for MLTE evaluation workflow
- NegotiationAgent: Generates QAS from agent specifications
- TestingAgent: Builds and executes test suites
- ValidationAgent: Validates evidence and generates results
- ReportingAgent: Creates comprehensive evaluation reports
- FederalComplianceAgent: Maps to NIST AI RMF and CMMC controls

Federal Compliance:
- CMMC Level 2
- NIST 800-171
- NIST AI RMF
- OSCAL export support

Example:
    >>> from agent_framework_mlte_integration import MLTEOrchestratorAgent
    >>> from agent_framework_mlte_integration.types import AgentSpec
    >>> from agent_framework_mlte_integration.config import MLTEConfig
    >>>
    >>> config = MLTEConfig.load()
    >>> orchestrator = MLTEOrchestratorAgent(
    ...     chat_client=client,
    ...     config=config,
    ...     enable_federal_compliance=True
    ... )
    >>> report = await orchestrator.run(agent_spec=my_agent_spec)

Copyright (c) 2025 Aurelius Tech & Talent Solutions
SDVOSB Certified | MBE Certified | Microsoft AI Cloud Partner
"""

from agent_framework_mlte_integration.config import MLTEConfig
from agent_framework_mlte_integration.orchestrator import MLTEOrchestratorAgent
from agent_framework_mlte_integration.types import (
    AgentSpec,
    ComplianceReport,
    EvaluationReport,
    EvaluationStatus,
    GateResult,
    QualityGate,
)

__version__ = "0.1.0"
__author__ = "Aurelius Tech & Talent Solutions"
__email__ = "info@aureliustech.com"

__all__ = [
    # Main orchestrator
    "MLTEOrchestratorAgent",
    # Configuration
    "MLTEConfig",
    # Types
    "AgentSpec",
    "ComplianceReport",
    "EvaluationReport",
    "EvaluationStatus",
    "GateResult",
    "QualityGate",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
]
