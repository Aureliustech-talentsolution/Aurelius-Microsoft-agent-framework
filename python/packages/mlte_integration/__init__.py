"""
MLTE Integration Package for Microsoft Agent Framework

Provides complete MLTE (Machine Learning Test & Evaluation) integration
for continuous testing and evaluation of AI agents.

Main Components:
    - MLTEOrchestrator: End-to-end evaluation coordinator
    - NegotiationAgent: QAS generation
    - TestingAgent: MLTE measurement execution
    - ValidationAgent: Quality gate evaluation
    - ReportingAgent: Multi-format report generation
    - FederalComplianceAgent: Federal framework mapping

Federal Compliance:
    - NIST AI RMF: 8 trustworthy AI characteristics
    - CMMC Level 2: Cybersecurity controls
    - NIST 800-53: Security controls
    - OSCAL: Automated documentation

Example:
    >>> from mlte_integration import MLTEOrchestrator
    >>> orchestrator = MLTEOrchestrator()
    >>> results = await orchestrator.evaluate_agent(agent_spec)
"""

__version__ = "0.1.0-alpha"
__author__ = "Aurelius Tech and Talent Solutions"

# Main orchestrator
from .orchestrator import MLTEOrchestrator, EvaluationContext, EvaluationPhase

# Core agents
from .agents.negotiation import NegotiationAgent
from .agents.testing import TestingAgent
from .agents.validation import ValidationAgent, QualityGate, Severity, Status
from .agents.reporting import ReportingAgent, ReportFormat
from .agents.federal_compliance import FederalComplianceAgent, ComplianceStatus

# Middleware and monitoring
from .agents.evaluation import MLTEEvaluationMiddleware
from .agents.runtime_monitor import RuntimeMonitor

# Lifecycle events
from .agents.lifecycle_events import (
    AgentLifecycleEvent,
    AgentLifecycleEventType,
)
from .agents.emitter import (
    LifecycleEventEmitter,
    register_lifecycle_listener,
    emit_lifecycle_event,
)

__all__ = [
    # Version
    "__version__",
    "__author__",
    
    # Main orchestrator
    "MLTEOrchestrator",
    "EvaluationContext",
    "EvaluationPhase",
    
    # Core agents
    "NegotiationAgent",
    "TestingAgent",
    "ValidationAgent",
    "ReportingAgent",
    "FederalComplianceAgent",
    
    # Validation types
    "QualityGate",
    "Severity",
    "Status",
    "ComplianceStatus",
    
    # Reporting types
    "ReportFormat",
    
    # Middleware and monitoring
    "MLTEEvaluationMiddleware",
    "RuntimeMonitor",
    
    # Lifecycle events
    "AgentLifecycleEvent",
    "AgentLifecycleEventType",
    "LifecycleEventEmitter",
    "register_lifecycle_listener",
    "emit_lifecycle_event",
]
