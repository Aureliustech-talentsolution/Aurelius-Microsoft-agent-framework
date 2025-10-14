"""
MLTEOrchestrator - End-to-End MLTE Integration Coordinator

Coordinates all MLTE agents to provide complete evaluation workflow:
1. NegotiationAgent - Generate QAS from agent spec
2. TestingAgent - Execute MLTE measurements
3. ValidationAgent - Apply quality gates
4. ReportingAgent - Generate reports
5. FederalComplianceAgent - Map to federal frameworks

Federal Compliance: CM-3 (Configuration Management), SA-11 (Developer Testing)
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class EvaluationPhase(Enum):
    """MLTE evaluation phases."""
    NEGOTIATION = "negotiation"
    TESTING = "testing"
    VALIDATION = "validation"
    REPORTING = "reporting"
    COMPLIANCE = "compliance"
    COMPLETE = "complete"


@dataclass
class EvaluationContext:
    """Context for MLTE evaluation."""
    agent_id: str
    agent_spec: Dict[str, Any]
    started_at: datetime = field(default_factory=datetime.utcnow)
    current_phase: EvaluationPhase = EvaluationPhase.NEGOTIATION
    
    # Results from each phase
    negotiation_card: Optional[Dict[str, Any]] = None
    test_results: Optional[Dict[str, Any]] = None
    validation_results: Optional[Dict[str, Any]] = None
    reports: Optional[Dict[str, Any]] = None
    compliance_results: Optional[Dict[str, Any]] = None
    
    # Status tracking
    completed_phases: List[EvaluationPhase] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    @property
    def is_complete(self) -> bool:
        """Check if evaluation is complete."""
        return self.current_phase == EvaluationPhase.COMPLETE
    
    @property
    def duration_seconds(self) -> float:
        """Get evaluation duration in seconds."""
        return (datetime.utcnow() - self.started_at).total_seconds()


class MLTEOrchestrator:
    """
    Orchestrates complete MLTE evaluation workflow.
    
    Workflow:
        1. Negotiation: Generate QAS from agent spec
        2. Testing: Execute MLTE measurements
        3. Validation: Apply quality gates
        4. Reporting: Generate comprehensive reports
        5. Compliance: Map to federal frameworks (NIST AI RMF, CMMC, NIST 800-53)
    
    Federal Compliance:
        - CM-3: Configuration Change Control
        - SA-11: Developer Security Testing and Evaluation
    
    Example:
        >>> orchestrator = MLTEOrchestrator()
        >>> results = await orchestrator.evaluate_agent(agent_spec)
        >>> print(f"Status: {results.validation_results['overall_status']}")
    """
    
    def __init__(
        self,
        output_dir: Optional[Path] = None,
        enable_compliance: bool = True,
    ):
        """
        Initialize MLTEOrchestrator.
        
        Args:
            output_dir: Directory for reports and artifacts
            enable_compliance: Whether to include federal compliance mapping
        """
        self.output_dir = output_dir or Path("mlte_output")
        self.enable_compliance = enable_compliance
        
        # Lazy-load agents (imported on first use)
        self._negotiation_agent = None
        self._testing_agent = None
        self._validation_agent = None
        self._reporting_agent = None
        self._compliance_agent = None
        
        logger.info("MLTEOrchestrator initialized (output: %s)", self.output_dir)
    
    async def evaluate_agent(
        self,
        agent_spec: Dict[str, Any],
        agent_id: Optional[str] = None,
    ) -> EvaluationContext:
        """
        Execute complete MLTE evaluation for an agent.
        
        Args:
            agent_spec: Agent specification (name, description, model_id, etc.)
            agent_id: Optional agent identifier
        
        Returns:
            EvaluationContext with results from all phases
        """
        agent_id = agent_id or agent_spec.get("name", "unknown")
        context = EvaluationContext(agent_id=agent_id, agent_spec=agent_spec)
        
        logger.info("="*70)
        logger.info("MLTE EVALUATION STARTED: %s", agent_id)
        logger.info("="*70)
        
        try:
            # Phase 1: Negotiation (QAS Generation)
            context = await self._phase_negotiation(context)
            
            # Phase 2: Testing (MLTE Measurements)
            context = await self._phase_testing(context)
            
            # Phase 3: Validation (Quality Gates)
            context = await self._phase_validation(context)
            
            # Phase 4: Reporting (Multi-format Reports)
            context = await self._phase_reporting(context)
            
            # Phase 5: Compliance (Federal Frameworks)
            if self.enable_compliance:
                context = await self._phase_compliance(context)
            
            # Mark complete
            context.current_phase = EvaluationPhase.COMPLETE
            
            logger.info("="*70)
            logger.info("MLTE EVALUATION COMPLETE: %s (%.2fs)", agent_id, context.duration_seconds)
            logger.info("="*70)
        
        except Exception as e:
            logger.error("MLTE evaluation failed: %s", str(e), exc_info=True)
            context.errors.append(str(e))
        
        return context
    
    async def _phase_negotiation(self, context: EvaluationContext) -> EvaluationContext:
        """Phase 1: Generate QAS using NegotiationAgent."""
        logger.info("\n📋 PHASE 1: NEGOTIATION (QAS Generation)")
        context.current_phase = EvaluationPhase.NEGOTIATION
        
        # Lazy load
        if self._negotiation_agent is None:
            from .negotiation import NegotiationAgent
            self._negotiation_agent = NegotiationAgent()
        
        # Generate QAS
        negotiation_card = await self._negotiation_agent.generate_qas(context.agent_spec)
        context.negotiation_card = negotiation_card
        context.completed_phases.append(EvaluationPhase.NEGOTIATION)
        
        logger.info("✅ Negotiation complete: %d QAS generated", len(negotiation_card.get("qas", [])))
        return context
    
    async def _phase_testing(self, context: EvaluationContext) -> EvaluationContext:
        """Phase 2: Execute tests using TestingAgent."""
        logger.info("\n🧪 PHASE 2: TESTING (MLTE Measurements)")
        context.current_phase = EvaluationPhase.TESTING
        
        # Lazy load
        if self._testing_agent is None:
            from .testing import TestingAgent
            self._testing_agent = TestingAgent()
        
        # Execute tests
        test_results = await self._testing_agent.execute_tests(
            context.negotiation_card,
            context.agent_spec,
        )
        context.test_results = test_results
        context.completed_phases.append(EvaluationPhase.TESTING)
        
        logger.info("✅ Testing complete: %d tests executed", test_results.get("test_count", 0))
        return context
    
    async def _phase_validation(self, context: EvaluationContext) -> EvaluationContext:
        """Phase 3: Validate using ValidationAgent."""
        logger.info("\n✔️  PHASE 3: VALIDATION (Quality Gates)")
        context.current_phase = EvaluationPhase.VALIDATION
        
        # Lazy load
        if self._validation_agent is None:
            from .validation import ValidationAgent
            self._validation_agent = ValidationAgent()
        
        # Validate results
        validation_results = await self._validation_agent.validate(
            context.test_results,
            context.agent_spec,
        )
        
        # Convert to dict for storage
        context.validation_results = {
            "overall_status": validation_results.overall_status.value,
            "gate_results": [
                {
                    "name": gr.gate_name,
                    "status": gr.status.value,
                    "severity": gr.severity.value,
                    "measured_value": gr.measured_value,
                    "expected_value": gr.expected_value,
                    "reasoning": gr.reasoning,
                    "remediation": gr.remediation,
                }
                for gr in validation_results.gate_results
            ],
            "validity_issues": validation_results.validity_issues,
            "warnings": validation_results.warnings,
            "recommendations": validation_results.recommendations,
        }
        context.completed_phases.append(EvaluationPhase.VALIDATION)
        
        logger.info("✅ Validation complete: %s", validation_results.overall_status.value)
        return context
    
    async def _phase_reporting(self, context: EvaluationContext) -> EvaluationContext:
        """Phase 4: Generate reports using ReportingAgent."""
        logger.info("\n📊 PHASE 4: REPORTING (Multi-format Reports)")
        context.current_phase = EvaluationPhase.REPORTING
        
        # Lazy load
        if self._reporting_agent is None:
            from .reporting import ReportingAgent, ReportFormat
            self._reporting_agent = ReportingAgent(
                output_dir=self.output_dir / context.agent_id,
                formats=[ReportFormat.MARKDOWN, ReportFormat.JSON, ReportFormat.HTML],
            )
        
        # Generate reports
        evaluation_results = {
            "negotiation_card": context.negotiation_card,
            "test_results": context.test_results,
            "validation_results": context.validation_results,
        }
        
        reports = await self._reporting_agent.generate_reports(
            evaluation_results,
            context.agent_spec,
        )
        context.reports = reports
        context.completed_phases.append(EvaluationPhase.REPORTING)
        
        report_count = len(reports.get("reports", [])) + len(reports.get("dashboards", []))
        logger.info("✅ Reporting complete: %d files generated", report_count)
        return context
    
    async def _phase_compliance(self, context: EvaluationContext) -> EvaluationContext:
        """Phase 5: Map to federal compliance using FederalComplianceAgent."""
        logger.info("\n🔒 PHASE 5: COMPLIANCE (Federal Frameworks)")
        context.current_phase = EvaluationPhase.COMPLIANCE
        
        # Lazy load
        if self._compliance_agent is None:
            from .federal_compliance import FederalComplianceAgent
            self._compliance_agent = FederalComplianceAgent()
        
        # Map compliance
        evaluation_results = {
            "negotiation_card": context.negotiation_card,
            "test_results": context.test_results,
            "validation_results": context.validation_results,
        }
        
        compliance_results = await self._compliance_agent.map_compliance(
            evaluation_results,
            context.agent_spec,
        )
        
        # Convert to dict for storage
        context.compliance_results = {
            "nist_ai_rmf": {
                char: status.value
                for char, status in compliance_results.nist_ai_rmf.characteristics.items()
            },
            "cmmc_l2": {
                control: status.value
                for control, status in compliance_results.cmmc_l2.controls.items()
            },
            "nist_800_53": {
                control: status.value
                for control, status in compliance_results.nist_800_53.controls.items()
            },
            "oscal_document": compliance_results.oscal_document,
        }
        context.completed_phases.append(EvaluationPhase.COMPLIANCE)
        
        logger.info("✅ Compliance complete: 3 frameworks mapped")
        return context


# Federal Compliance Annotations
MLTEOrchestrator.__annotations__["federal_compliance"] = {
    "CM-3": "Configuration Change Control - Manages agent evaluation configuration",
    "SA-11": "Developer Security Testing and Evaluation - Orchestrates complete testing",
}
