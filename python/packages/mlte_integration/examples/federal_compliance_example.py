"""
Example: Using FederalComplianceAgent to map evaluation results to federal frameworks.

Federal Compliance: CA-2, CA-7, SA-11
"""

import asyncio
import json
from mlte_integration.agents.federal_compliance import FederalComplianceAgent, ComplianceStatus


async def main():
    """Demonstrate FederalComplianceAgent usage."""
    
    # Sample evaluation results (from ValidationAgent)
    evaluation_results = {
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
                    "name": "PII Leakage Prevention",
                    "status": "PASS",
                    "severity": "blocking",
                },
                {
                    "name": "Demographic Parity",
                    "status": "WARNING",
                    "severity": "warning",
                },
                {
                    "name": "Response Latency",
                    "status": "PASS",
                    "severity": "warning",
                },
            ],
        },
    }
    
    print("\n" + "="*80)
    print("MLTE FederalComplianceAgent - Federal Framework Mapping")
    print("="*80)
    
    # Initialize FederalComplianceAgent
    agent = FederalComplianceAgent()
    
    print("\n🔍 Mapping evaluation results to federal frameworks...")
    print("   - NIST AI RMF (8 characteristics)")
    print("   - CMMC Level 2 (7 AI-relevant controls)")
    print("   - NIST 800-53 (4 AI-relevant controls)")
    
    # Map compliance
    results = await agent.map_compliance(
        evaluation_results,
        agent_spec={"name": "SecurityAgent", "version": "1.0.0"},
    )
    
    # Display NIST AI RMF Results
    print("\n" + "-"*80)
    print("📋 NIST AI RMF CHARACTERISTICS")
    print("-"*80)
    
    for char, status in results.nist_ai_rmf.characteristics.items():
        icon = "✅" if status == ComplianceStatus.PASS else "❌" if status == ComplianceStatus.FAIL else "⚠️" if status == ComplianceStatus.WARNING else "ℹ️"
        print(f"{icon} {char}: {status.value.upper()}")
        
        # Show evidence
        if char in results.nist_ai_rmf.evidence:
            evidence = results.nist_ai_rmf.evidence[char]
            if evidence:
                print(f"   Evidence: {evidence[0]}")
        
        # Show gaps
        if char in results.nist_ai_rmf.gaps:
            gaps = results.nist_ai_rmf.gaps[char]
            if gaps:
                print(f"   Gap: {gaps[0]}")
    
    # Display CMMC L2 Results
    print("\n" + "-"*80)
    print("🛡️  CMMC LEVEL 2 CONTROLS")
    print("-"*80)
    
    for control, status in results.cmmc_l2.controls.items():
        icon = "✅" if status == ComplianceStatus.PASS else "❌" if status == ComplianceStatus.FAIL else "⚠️"
        control_name = results.cmmc_l2.implementation_notes.get(control, "")
        print(f"{icon} {control}: {status.value.upper()}")
        print(f"   {control_name}")
    
    # Display NIST 800-53 Results
    print("\n" + "-"*80)
    print("🔐 NIST 800-53 SECURITY CONTROLS")
    print("-"*80)
    
    for control, status in results.nist_800_53.controls.items():
        icon = "✅" if status == ComplianceStatus.PASS else "❌"
        print(f"{icon} {control}: {status.value.upper()}")
    
    # Display OSCAL Summary
    print("\n" + "-"*80)
    print("📄 OSCAL ASSESSMENT RESULTS")
    print("-"*80)
    
    if results.oscal_document:
        findings_count = len(results.oscal_document["assessment-results"]["results"][0]["findings"])
        print(f"   Total Findings: {findings_count}")
        print(f"   Document UUID: {results.oscal_document['assessment-results']['uuid']}")
        
        if findings_count > 0:
            print("\n   Top Findings:")
            for finding in results.oscal_document["assessment-results"]["results"][0]["findings"][:3]:
                print(f"     • {finding['title']}")
    
    # Compliance Summary
    print("\n" + "="*80)
    print("📊 COMPLIANCE SUMMARY")
    print("="*80)
    
    nist_ai_rmf_failures = sum(1 for s in results.nist_ai_rmf.characteristics.values() if s == ComplianceStatus.FAIL)
    cmmc_failures = sum(1 for s in results.cmmc_l2.controls.values() if s == ComplianceStatus.FAIL)
    
    print(f"   NIST AI RMF: {len(results.nist_ai_rmf.characteristics) - nist_ai_rmf_failures}/{len(results.nist_ai_rmf.characteristics)} characteristics PASS")
    print(f"   CMMC L2: {len(results.cmmc_l2.controls) - cmmc_failures}/{len(results.cmmc_l2.controls)} controls PASS")
    print(f"   NIST 800-53: {len(results.nist_800_53.controls)}/{len(results.nist_800_53.controls)} controls PASS")
    
    if nist_ai_rmf_failures > 0 or cmmc_failures > 0:
        print("\n⚠️  COMPLIANCE GAPS DETECTED")
        print("   Review findings and implement recommended remediations")
    else:
        print("\n✅ FULL COMPLIANCE ACHIEVED")
        print("   Agent meets all federal framework requirements")
    
    print("="*80)
    
    # Federal Compliance Note
    print("\n📋 Federal Compliance:")
    print("   - CA-2: Security Assessments")
    print("   - CA-7: Continuous Monitoring")
    print("   - SA-11: Developer Security Testing and Evaluation")
    
    # Save OSCAL document
    if results.oscal_document:
        oscal_path = "oscal_assessment_results.json"
        with open(oscal_path, "w") as f:
            json.dump(results.oscal_document, f, indent=2)
        print(f"\n💾 OSCAL document saved to: {oscal_path}")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
