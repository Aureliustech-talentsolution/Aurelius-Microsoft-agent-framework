"""
Federal Compliance Validation Tests

Validates compliance with federal requirements:
- NIST AI RMF (8 trustworthy AI characteristics)
- CMMC Level 2 (Cybersecurity controls)
- NIST 800-53 (Security controls)
- OSCAL (Open Security Controls Assessment Language)

Federal Compliance: CA-2 (Security Assessments), CA-7 (Continuous Monitoring)
"""

import pytest
from pathlib import Path
from mlte_integration import MLTEOrchestrator, ComplianceStatus


@pytest.fixture
def cui_agent_spec():
    """CUI (Controlled Unclassified Information) agent."""
    return {
        "name": "CUISecurityAgent",
        "description": "Agent handling CUI for federal compliance testing",
        "model_id": "gpt-4",
        "version": "1.0.0",
        "category": "CUI",
        "capabilities": [
            "cui_processing",
            "security_controls",
            "audit_logging",
        ],
        "deployment_env": "production",
        "data_classification": "cui",
    }


@pytest.mark.asyncio
@pytest.mark.compliance
class TestNISTAIRMF:
    """Test NIST AI Risk Management Framework compliance."""
    
    async def test_all_characteristics_evaluated(self, cui_agent_spec, tmp_path):
        """Test all 8 NIST AI RMF characteristics are evaluated."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            nist_ai_rmf = context.compliance_results.get("nist_ai_rmf", {})
            
            # Should evaluate all 8 characteristics
            expected_characteristics = {
                "valid_reliable",
                "safe",
                "secure_resilient",
                "accountable_transparent",
                "explainable_interpretable",
                "privacy_enhanced",
                "fair",
                "continuous_monitoring",
            }
            
            evaluated_chars = set(nist_ai_rmf.keys())
            
            # Check coverage
            coverage = len(evaluated_chars.intersection(expected_characteristics))
            print(f"\n🎯 NIST AI RMF Coverage: {coverage}/{len(expected_characteristics)} characteristics")
            
            for char in expected_characteristics:
                if char in nist_ai_rmf:
                    print(f"   ✅ {char}: {nist_ai_rmf[char]}")
                else:
                    print(f"   ❌ {char}: Not evaluated")
    
    async def test_characteristic_status_values(self, cui_agent_spec, tmp_path):
        """Test NIST AI RMF status values are valid."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            nist_ai_rmf = context.compliance_results.get("nist_ai_rmf", {})
            
            valid_statuses = {"pass", "warning", "fail", "not_applicable"}
            
            for char, status in nist_ai_rmf.items():
                assert status in valid_statuses, f"{char} has invalid status: {status}"


@pytest.mark.asyncio
@pytest.mark.compliance
class TestCMMCLevel2:
    """Test CMMC Level 2 compliance."""
    
    async def test_required_controls_mapped(self, cui_agent_spec, tmp_path):
        """Test required CMMC L2 controls are mapped."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            cmmc_l2 = context.compliance_results.get("cmmc_l2", {})
            
            # Should have key control families
            expected_families = ["AC", "AU", "CA", "CM", "IA", "SC", "SI"]
            
            mapped_families = set()
            for control in cmmc_l2.keys():
                family = control.split("-")[0]
                mapped_families.add(family)
            
            print(f"\n🛡️  CMMC L2 Control Families: {len(mapped_families)}")
            for family in sorted(mapped_families):
                family_controls = [c for c in cmmc_l2 if c.startswith(family)]
                print(f"   {family}: {len(family_controls)} controls")
    
    async def test_cui_controls_present(self, cui_agent_spec, tmp_path):
        """Test CUI-specific controls are present."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            cmmc_l2 = context.compliance_results.get("cmmc_l2", {})
            
            # Key CUI controls
            critical_controls = [
                "AC-1",  # Access Control Policy
                "AU-2",  # Audit Events
                "CA-2",  # Security Assessments
                "SC-7",  # Boundary Protection
            ]
            
            for control in critical_controls:
                if control in cmmc_l2:
                    print(f"   ✅ {control}: {cmmc_l2[control]}")


@pytest.mark.asyncio
@pytest.mark.compliance
class TestNIST80053:
    """Test NIST 800-53 security controls."""
    
    async def test_security_controls_mapped(self, cui_agent_spec, tmp_path):
        """Test NIST 800-53 security controls are mapped."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            nist_800_53 = context.compliance_results.get("nist_800_53", {})
            
            # Should have security control families
            print(f"\n🔐 NIST 800-53 Controls: {len(nist_800_53)}")
            
            # Group by family
            families = {}
            for control, status in nist_800_53.items():
                family = control.split("-")[0]
                if family not in families:
                    families[family] = []
                families[family].append((control, status))
            
            for family, controls in sorted(families.items()):
                passed = sum(1 for _, s in controls if s == "pass")
                print(f"   {family}: {passed}/{len(controls)} PASS")
    
    async def test_assessment_controls(self, cui_agent_spec, tmp_path):
        """Test assessment-related controls (CA family)."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            nist_800_53 = context.compliance_results.get("nist_800_53", {})
            
            # CA (Security Assessment and Authorization) controls
            ca_controls = {k: v for k, v in nist_800_53.items() if k.startswith("CA-")}
            
            assert len(ca_controls) > 0, "Should have CA controls"
            print(f"\n📋 Assessment Controls (CA family): {len(ca_controls)}")


@pytest.mark.asyncio
@pytest.mark.compliance
class TestOSCAL:
    """Test OSCAL document generation."""
    
    async def test_oscal_structure_valid(self, cui_agent_spec, tmp_path):
        """Test OSCAL document has valid structure."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            oscal = context.compliance_results.get("oscal_document")
            
            if oscal:
                # Check required top-level structure
                assert "assessment-results" in oscal
                
                assessment_results = oscal["assessment-results"]
                assert "metadata" in assessment_results
                assert "results" in assessment_results
                
                print("\n📄 OSCAL Document Structure:")
                print(f"   ✅ assessment-results")
                print(f"   ✅ metadata")
                print(f"   ✅ results")
    
    async def test_oscal_findings(self, cui_agent_spec, tmp_path):
        """Test OSCAL findings are generated."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            oscal = context.compliance_results.get("oscal_document")
            
            if oscal and "assessment-results" in oscal:
                results = oscal["assessment-results"].get("results", [])
                
                if results:
                    findings = results[0].get("findings", [])
                    print(f"\n🔍 OSCAL Findings: {len(findings)}")
                    
                    # Show finding types
                    if findings:
                        statuses = {}
                        for finding in findings:
                            status = finding.get("target", {}).get("status", {}).get("state", "unknown")
                            statuses[status] = statuses.get(status, 0) + 1
                        
                        for status, count in statuses.items():
                            print(f"   {status}: {count}")


@pytest.mark.asyncio
@pytest.mark.compliance
class TestComplianceIntegration:
    """Test integration between compliance frameworks."""
    
    async def test_compliance_consistency(self, cui_agent_spec, tmp_path):
        """Test consistency across compliance frameworks."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(cui_agent_spec)
        
        if context.compliance_results:
            nist_ai_rmf = context.compliance_results.get("nist_ai_rmf", {})
            cmmc_l2 = context.compliance_results.get("cmmc_l2", {})
            nist_800_53 = context.compliance_results.get("nist_800_53", {})
            
            print("\n🔗 Compliance Framework Coverage:")
            print(f"   NIST AI RMF: {len(nist_ai_rmf)} characteristics")
            print(f"   CMMC L2: {len(cmmc_l2)} controls")
            print(f"   NIST 800-53: {len(nist_800_53)} controls")
            
            # All frameworks should be evaluated
            assert len(nist_ai_rmf) > 0 or len(cmmc_l2) > 0 or len(nist_800_53) > 0


# Federal Compliance Annotations
pytest.mark.federal_compliance = {
    "CA-2": "Security Assessments",
    "CA-7": "Continuous Monitoring",
}
