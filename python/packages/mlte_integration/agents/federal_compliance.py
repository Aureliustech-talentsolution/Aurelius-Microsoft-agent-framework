"""
FederalComplianceAgent - Federal Compliance Mapping Coordinator

Coordinates compliance mapping using 3 sub-agents:
1. CMMCMappingSubAgent - Maps to CMMC Level 2 controls
2. NIST80053SubAgent - Maps to NIST 800-53 security controls
3. NISTAIRMFSubAgent - Maps to NIST AI RMF characteristics

Federal Compliance: CA-2 (Security Assessments), CA-7 (Continuous Monitoring), SA-11
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance status."""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "not_applicable"
    PARTIAL = "partial"


@dataclass
class NISTAIRMFMapping:
    """NIST AI RMF characteristics mapping."""
    characteristics: Dict[str, ComplianceStatus] = field(default_factory=dict)
    evidence: Dict[str, List[str]] = field(default_factory=dict)
    gaps: Dict[str, List[str]] = field(default_factory=dict)
    recommendations: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class CMMCMapping:
    """CMMC Level 2 controls mapping."""
    controls: Dict[str, ComplianceStatus] = field(default_factory=dict)
    evidence: Dict[str, List[str]] = field(default_factory=dict)
    gaps: Dict[str, List[str]] = field(default_factory=dict)
    implementation_notes: Dict[str, str] = field(default_factory=dict)


@dataclass
class NIST80053Mapping:
    """NIST 800-53 security controls mapping."""
    controls: Dict[str, ComplianceStatus] = field(default_factory=dict)
    evidence: Dict[str, List[str]] = field(default_factory=dict)
    gaps: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class ComplianceResults:
    """Complete federal compliance mapping results."""
    nist_ai_rmf: NISTAIRMFMapping
    cmmc_l2: CMMCMapping
    nist_800_53: NIST80053Mapping
    timestamp: datetime = field(default_factory=datetime.utcnow)
    oscal_document: Optional[Dict[str, Any]] = None


class FederalComplianceAgent:
    """
    Coordinates federal compliance mapping.
    
    Architecture:
        FederalComplianceAgent (Coordinator)
        ├→ NISTAIRMFSubAgent: Maps to NIST AI RMF 8 characteristics
        ├→ CMMCMappingSubAgent: Maps to CMMC Level 2 controls
        └→ NIST80053SubAgent: Maps to NIST 800-53 controls
    
    Federal Compliance:
        - CA-2: Security Assessments
        - CA-7: Continuous Monitoring
        - SA-11: Developer Security Testing and Evaluation
    """
    
    def __init__(self):
        """Initialize FederalComplianceAgent."""
        self.nist_ai_rmf_agent = None  # Lazy init
        self.cmmc_agent = None  # Lazy init
        self.nist_800_53_agent = None  # Lazy init
        
        logger.info("FederalComplianceAgent initialized")
    
    async def map_compliance(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]] = None,
    ) -> ComplianceResults:
        """
        Map evaluation results to federal compliance frameworks.
        
        Args:
            evaluation_results: Complete evaluation results from all agents
            agent_spec: Optional agent specification
        
        Returns:
            ComplianceResults with mappings to all frameworks
        """
        logger.info("Starting federal compliance mapping")
        
        # Lazy import sub-agents
        if self.nist_ai_rmf_agent is None:
            from .compliance_subagents import (
                NISTAIRMFSubAgent,
                CMMCMappingSubAgent,
                NIST80053SubAgent,
            )
            self.nist_ai_rmf_agent = NISTAIRMFSubAgent()
            self.cmmc_agent = CMMCMappingSubAgent()
            self.nist_800_53_agent = NIST80053SubAgent()
        
        # Map to each framework in parallel
        import asyncio
        nist_ai_rmf, cmmc_l2, nist_800_53 = await asyncio.gather(
            self.nist_ai_rmf_agent.map_to_ai_rmf(evaluation_results, agent_spec),
            self.cmmc_agent.map_to_cmmc(evaluation_results, agent_spec),
            self.nist_800_53_agent.map_to_nist_800_53(evaluation_results, agent_spec),
        )
        
        # Generate OSCAL document
        oscal_doc = self._generate_oscal(nist_ai_rmf, cmmc_l2, nist_800_53, agent_spec)
        
        results = ComplianceResults(
            nist_ai_rmf=nist_ai_rmf,
            cmmc_l2=cmmc_l2,
            nist_800_53=nist_800_53,
            oscal_document=oscal_doc,
        )
        
        logger.info("Federal compliance mapping complete")
        
        return results
    
    def _generate_oscal(
        self,
        nist_ai_rmf: NISTAIRMFMapping,
        cmmc_l2: CMMCMapping,
        nist_800_53: NIST80053Mapping,
        agent_spec: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate OSCAL assessment results document."""
        import uuid
        
        agent_name = agent_spec.get("name", "Agent") if agent_spec else "Agent"
        
        findings = []
        
        # Add NIST AI RMF findings
        for char, status in nist_ai_rmf.characteristics.items():
            if status in [ComplianceStatus.FAIL, ComplianceStatus.WARNING]:
                findings.append({
                    "uuid": str(uuid.uuid4()),
                    "title": f"NIST AI RMF: {char} - {status.value.upper()}",
                    "description": ", ".join(nist_ai_rmf.gaps.get(char, [])),
                    "target": {
                        "type": "component",
                        "target-id": agent_name,
                    },
                })
        
        # Add CMMC findings
        for control, status in cmmc_l2.controls.items():
            if status != ComplianceStatus.PASS:
                findings.append({
                    "uuid": str(uuid.uuid4()),
                    "title": f"CMMC L2 {control}: {status.value.upper()}",
                    "description": ", ".join(cmmc_l2.gaps.get(control, [])),
                })
        
        oscal_doc = {
            "assessment-results": {
                "uuid": str(uuid.uuid4()),
                "metadata": {
                    "title": f"MLTE Compliance Assessment - {agent_name}",
                    "last-modified": datetime.utcnow().isoformat(),
                    "version": "1.0.0",
                    "oscal-version": "1.1.2",
                },
                "results": [{
                    "uuid": str(uuid.uuid4()),
                    "title": "MLTE Automated Compliance Mapping",
                    "description": "Federal compliance framework mappings",
                    "start": datetime.utcnow().isoformat(),
                    "end": datetime.utcnow().isoformat(),
                    "findings": findings,
                }],
            }
        }
        
        return oscal_doc


# Federal Compliance Annotations
FederalComplianceAgent.__annotations__["federal_compliance"] = {
    "CA-2": "Security Assessments - Compliance mapping and assessment",
    "CA-7": "Continuous Monitoring - Ongoing compliance verification",
    "SA-11": "Developer Security Testing and Evaluation",
}
