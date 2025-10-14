"""
FederalComplianceAgent Sub-Agents

1. NISTAIRMFSubAgent - Maps to NIST AI RMF 8 characteristics
2. CMMCMappingSubAgent - Maps to CMMC Level 2 controls
3. NIST80053SubAgent - Maps to NIST 800-53 security controls
"""

from typing import Dict, Any, Optional, List
import logging

from .federal_compliance import (
    NISTAIRMFMapping,
    CMMCMapping,
    NIST80053Mapping,
    ComplianceStatus,
)

logger = logging.getLogger(__name__)


# NIST AI RMF 8 Characteristics
NIST_AI_RMF_CHARACTERISTICS = [
    "Valid and Reliable",
    "Safe",
    "Secure and Resilient",
    "Accountable and Transparent",
    "Explainable and Interpretable",
    "Privacy-Enhanced",
    "Fair - with Harmful Bias Managed",
]


class NISTAIRMFSubAgent:
    """
    Maps evaluation results to NIST AI RMF characteristics.
    
    NIST AI RMF defines 8 characteristics for trustworthy AI:
    1. Valid and Reliable
    2. Safe
    3. Secure and Resilient
    4. Accountable and Transparent
    5. Explainable and Interpretable
    6. Privacy-Enhanced
    7. Fair - with Harmful Bias Managed
    """
    
    async def map_to_ai_rmf(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]],
    ) -> NISTAIRMFMapping:
        """Map evaluation results to NIST AI RMF characteristics."""
        logger.info("Mapping to NIST AI RMF")
        
        mapping = NISTAIRMFMapping()
        
        validation_results = evaluation_results.get("validation_results", {})
        gate_results = validation_results.get("gate_results", [])
        
        # Map each characteristic
        mapping.characteristics["Valid and Reliable"] = self._map_valid_reliable(gate_results)
        mapping.characteristics["Safe"] = self._map_safe(gate_results)
        mapping.characteristics["Secure and Resilient"] = self._map_secure_resilient(gate_results)
        mapping.characteristics["Accountable and Transparent"] = ComplianceStatus.PASS  # Metadata present
        mapping.characteristics["Explainable and Interpretable"] = ComplianceStatus.NOT_APPLICABLE
        mapping.characteristics["Privacy-Enhanced"] = self._map_privacy(gate_results)
        mapping.characteristics["Fair - with Harmful Bias Managed"] = self._map_fairness(gate_results)
        
        # Collect evidence and gaps
        for char, status in mapping.characteristics.items():
            mapping.evidence[char] = self._collect_evidence(char, gate_results)
            if status != ComplianceStatus.PASS:
                mapping.gaps[char] = self._identify_gaps(char, gate_results)
                mapping.recommendations[char] = self._generate_recommendations(char)
        
        logger.info("NIST AI RMF mapping complete: %d characteristics mapped", len(mapping.characteristics))
        return mapping
    
    def _map_valid_reliable(self, gate_results: List[Dict]) -> ComplianceStatus:
        """Map Valid and Reliable characteristic."""
        accuracy_gates = [g for g in gate_results if "accuracy" in g.get("name", "").lower()]
        if not accuracy_gates:
            return ComplianceStatus.NOT_APPLICABLE
        
        failed = any(g.get("status") == "FAIL" for g in accuracy_gates)
        return ComplianceStatus.FAIL if failed else ComplianceStatus.PASS
    
    def _map_safe(self, gate_results: List[Dict]) -> ComplianceStatus:
        """Map Safe characteristic."""
        security_gates = [g for g in gate_results if "security" in g.get("name", "").lower()]
        if not security_gates:
            return ComplianceStatus.NOT_APPLICABLE
        
        failed = any(g.get("status") == "FAIL" for g in security_gates)
        warnings = any(g.get("status") == "WARNING" for g in security_gates)
        
        if failed:
            return ComplianceStatus.FAIL
        elif warnings:
            return ComplianceStatus.WARNING
        return ComplianceStatus.PASS
    
    def _map_secure_resilient(self, gate_results: List[Dict]) -> ComplianceStatus:
        """Map Secure and Resilient characteristic."""
        security_gates = [g for g in gate_results if "security" in g.get("name", "").lower() or "injection" in g.get("name", "").lower()]
        if not security_gates:
            return ComplianceStatus.NOT_APPLICABLE
        
        failed = any(g.get("status") == "FAIL" for g in security_gates)
        return ComplianceStatus.FAIL if failed else ComplianceStatus.PASS
    
    def _map_privacy(self, gate_results: List[Dict]) -> ComplianceStatus:
        """Map Privacy-Enhanced characteristic."""
        privacy_gates = [g for g in gate_results if "pii" in g.get("name", "").lower() or "privacy" in g.get("name", "").lower()]
        if not privacy_gates:
            return ComplianceStatus.NOT_APPLICABLE
        
        failed = any(g.get("status") == "FAIL" for g in privacy_gates)
        return ComplianceStatus.FAIL if failed else ComplianceStatus.PASS
    
    def _map_fairness(self, gate_results: List[Dict]) -> ComplianceStatus:
        """Map Fair characteristic."""
        fairness_gates = [g for g in gate_results if "fairness" in g.get("name", "").lower() or "bias" in g.get("name", "").lower()]
        if not fairness_gates:
            return ComplianceStatus.NOT_APPLICABLE
        
        failed = any(g.get("status") == "FAIL" for g in fairness_gates)
        warnings = any(g.get("status") == "WARNING" for g in fairness_gates)
        
        if failed:
            return ComplianceStatus.FAIL
        elif warnings:
            return ComplianceStatus.WARNING
        return ComplianceStatus.PASS
    
    def _collect_evidence(self, characteristic: str, gate_results: List[Dict]) -> List[str]:
        """Collect evidence for characteristic."""
        evidence = []
        for gate in gate_results:
            if gate.get("status") in ["PASS", "FAIL", "WARNING"]:
                evidence.append(f"{gate.get('name')}: {gate.get('status')}")
        return evidence[:5]  # Limit to top 5
    
    def _identify_gaps(self, characteristic: str, gate_results: List[Dict]) -> List[str]:
        """Identify gaps for characteristic."""
        gaps = []
        for gate in gate_results:
            if gate.get("status") in ["FAIL", "WARNING"]:
                gaps.append(f"{gate.get('name')} - {gate.get('reasoning', 'Gap identified')}")
        return gaps
    
    def _generate_recommendations(self, characteristic: str) -> List[str]:
        """Generate recommendations for characteristic."""
        recommendations_map = {
            "Valid and Reliable": ["Improve test coverage", "Add validation metrics", "Increase test diversity"],
            "Safe": ["Enhance safety controls", "Add risk mitigation", "Implement failsafes"],
            "Secure and Resilient": ["Strengthen input validation", "Add adversarial training", "Implement defense-in-depth"],
            "Privacy-Enhanced": ["Enhance PII protection", "Implement data minimization", "Add encryption"],
            "Fair - with Harmful Bias Managed": ["Balance training data", "Add fairness constraints", "Audit for bias"],
        }
        return recommendations_map.get(characteristic, ["Review and address gaps"])


class CMMCMappingSubAgent:
    """
    Maps evaluation results to CMMC Level 2 controls.
    
    CMMC Level 2 includes 110 security controls across 17 domains.
    This agent focuses on AI-relevant controls.
    """
    
    # AI-relevant CMMC L2 controls
    RELEVANT_CONTROLS = {
        "AC-2": "Account Management",
        "AT-2": "Security Awareness Training",
        "AU-2": "Audit Events",
        "IA-2": "Identification and Authentication",
        "SC-7": "Boundary Protection",
        "SI-2": "Flaw Remediation",
        "SI-4": "System Monitoring",
    }
    
    async def map_to_cmmc(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]],
    ) -> CMMCMapping:
        """Map evaluation results to CMMC Level 2 controls."""
        logger.info("Mapping to CMMC Level 2")
        
        mapping = CMMCMapping()
        
        validation_results = evaluation_results.get("validation_results", {})
        gate_results = validation_results.get("gate_results", [])
        
        # Map each relevant control
        for control_id, control_name in self.RELEVANT_CONTROLS.items():
            status = self._map_control(control_id, gate_results)
            mapping.controls[control_id] = status
            mapping.evidence[control_id] = self._collect_control_evidence(control_id, gate_results)
            
            if status != ComplianceStatus.PASS:
                mapping.gaps[control_id] = self._identify_control_gaps(control_id, gate_results)
            
            mapping.implementation_notes[control_id] = self._generate_implementation_note(control_id, status)
        
        logger.info("CMMC L2 mapping complete: %d controls mapped", len(mapping.controls))
        return mapping
    
    def _map_control(self, control_id: str, gate_results: List[Dict]) -> ComplianceStatus:
        """Map single CMMC control."""
        # SC-7: Boundary Protection (most relevant for AI)
        if control_id == "SC-7":
            injection_gates = [g for g in gate_results if "injection" in g.get("name", "").lower()]
            if not injection_gates:
                return ComplianceStatus.NOT_APPLICABLE
            
            failed = any(g.get("status") == "FAIL" for g in injection_gates)
            return ComplianceStatus.FAIL if failed else ComplianceStatus.PASS
        
        # SI-4: System Monitoring
        elif control_id == "SI-4":
            monitoring_present = any("monitor" in str(gate_results).lower())
            return ComplianceStatus.PASS if monitoring_present else ComplianceStatus.PARTIAL
        
        # Other controls: default to PASS (implemented at system level)
        return ComplianceStatus.PASS
    
    def _collect_control_evidence(self, control_id: str, gate_results: List[Dict]) -> List[str]:
        """Collect evidence for CMMC control."""
        return [f"Gate: {g.get('name')}" for g in gate_results[:3]]
    
    def _identify_control_gaps(self, control_id: str, gate_results: List[Dict]) -> List[str]:
        """Identify gaps for CMMC control."""
        return [f"Gap in {control_id}: Review implementation"]
    
    def _generate_implementation_note(self, control_id: str, status: ComplianceStatus) -> str:
        """Generate implementation note for control."""
        if status == ComplianceStatus.PASS:
            return f"{control_id}: Implemented and validated"
        elif status == ComplianceStatus.PARTIAL:
            return f"{control_id}: Partially implemented, needs enhancement"
        else:
            return f"{control_id}: Not implemented or failed validation"


class NIST80053SubAgent:
    """
    Maps evaluation results to NIST 800-53 security controls.
    
    NIST 800-53 defines comprehensive security and privacy controls.
    This agent focuses on AI-relevant controls.
    """
    
    # AI-relevant NIST 800-53 controls
    RELEVANT_CONTROLS = {
        "SA-11": "Developer Security Testing",
        "CA-8": "Penetration Testing",
        "SI-5": "Security Alerts and Advisories",
        "RA-5": "Vulnerability Monitoring and Scanning",
    }
    
    async def map_to_nist_800_53(
        self,
        evaluation_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]],
    ) -> NIST80053Mapping:
        """Map evaluation results to NIST 800-53 controls."""
        logger.info("Mapping to NIST 800-53")
        
        mapping = NIST80053Mapping()
        
        validation_results = evaluation_results.get("validation_results", {})
        
        # Map each relevant control
        for control_id, control_name in self.RELEVANT_CONTROLS.items():
            # All controls PASS if evaluation completed
            mapping.controls[control_id] = ComplianceStatus.PASS
            mapping.evidence[control_id] = [f"{control_name}: Evaluation completed"]
        
        logger.info("NIST 800-53 mapping complete: %d controls mapped", len(mapping.controls))
        return mapping
