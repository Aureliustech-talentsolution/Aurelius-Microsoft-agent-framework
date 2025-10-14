"""
Example: Complete MLTE evaluation workflow using MLTEOrchestrator.

This example demonstrates the end-to-end evaluation of an AI agent including:
1. QAS generation
2. MLTE testing
3. Quality gate validation
4. Report generation
5. Federal compliance mapping

Federal Compliance: CM-3, SA-11
"""

import asyncio
from pathlib import Path
from mlte_integration.orchestrator import MLTEOrchestrator, EvaluationPhase


async def main():
    """Demonstrate complete MLTE evaluation workflow."""
    
    # Define agent specification
    agent_spec = {
        "name": "CustomerSupportAgent",
        "description": "AI agent for customer support and inquiry resolution",
        "model_id": "gpt-4",
        "version": "1.0.0",
        "category": "CUI",  # Controlled Unclassified Information
        "capabilities": [
            "customer_inquiry_resolution",
            "ticket_categorization",
            "knowledge_base_search",
        ],
        "deployment_env": "production",
        "data_classification": "confidential",
    }
    
    print("\n" + "="*80)
    print("MLTE ORCHESTRATOR - COMPLETE EVALUATION WORKFLOW")
    print("="*80)
    print(f"\nAgent: {agent_spec['name']}")
    print(f"Model: {agent_spec['model_id']}")
    print(f"Category: {agent_spec['category']}")
    print(f"Capabilities: {', '.join(agent_spec['capabilities'])}")
    
    # Initialize orchestrator
    output_dir = Path("mlte_evaluation_output")
    orchestrator = MLTEOrchestrator(
        output_dir=output_dir,
        enable_compliance=True,  # Include federal compliance mapping
    )
    
    print(f"\n📂 Output Directory: {output_dir}")
    print("\n🚀 Starting MLTE evaluation...")
    
    # Execute complete evaluation
    context = await orchestrator.evaluate_agent(
        agent_spec=agent_spec,
        agent_id="customer_support_agent_v1",
    )
    
    # Display results
    print("\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)
    
    print(f"\n⏱️  Duration: {context.duration_seconds:.2f} seconds")
    print(f"📊 Completed Phases: {len(context.completed_phases)}/5")
    
    for phase in context.completed_phases:
        print(f"   ✅ {phase.value.upper()}")
    
    if context.errors:
        print(f"\n❌ Errors: {len(context.errors)}")
        for error in context.errors:
            print(f"   • {error}")
    
    # Phase-specific results
    if context.negotiation_card:
        print("\n" + "-"*80)
        print("1️⃣  NEGOTIATION RESULTS")
        print("-"*80)
        qas_count = len(context.negotiation_card.get("qas", []))
        print(f"   QAS Generated: {qas_count}")
        if qas_count > 0:
            print(f"   Sample QAS: {context.negotiation_card['qas'][0].get('scenario', 'N/A')[:100]}...")
    
    if context.test_results:
        print("\n" + "-"*80)
        print("2️⃣  TESTING RESULTS")
        print("-"*80)
        print(f"   Tests Executed: {context.test_results.get('test_count', 0)}")
        print(f"   Test Types: {', '.join(context.test_results.get('test_types', []))}")
    
    if context.validation_results:
        print("\n" + "-"*80)
        print("3️⃣  VALIDATION RESULTS")
        print("-"*80)
        status = context.validation_results.get("overall_status", "UNKNOWN")
        gate_results = context.validation_results.get("gate_results", [])
        passed = sum(1 for g in gate_results if g.get("status") == "pass")
        
        status_icon = "✅" if status == "pass" else "❌" if status == "fail" else "⚠️"
        print(f"   Overall Status: {status_icon} {status.upper()}")
        print(f"   Quality Gates: {passed}/{len(gate_results)} PASSED")
        
        # Show blocking failures
        blocking_failures = [
            g for g in gate_results
            if g.get("status") == "fail" and g.get("severity") == "blocking"
        ]
        if blocking_failures:
            print(f"\n   🚫 Blocking Failures:")
            for failure in blocking_failures:
                print(f"      • {failure.get('name')}: {failure.get('reasoning')}")
    
    if context.reports:
        print("\n" + "-"*80)
        print("4️⃣  REPORTING RESULTS")
        print("-"*80)
        reports = context.reports.get("reports", [])
        dashboards = context.reports.get("dashboards", [])
        
        print(f"   Reports Generated: {len(reports)}")
        for report_path in reports:
            print(f"      📄 {report_path}")
        
        if dashboards:
            print(f"   Dashboards Generated: {len(dashboards)}")
            for dashboard_path in dashboards:
                print(f"      📊 {dashboard_path}")
    
    if context.compliance_results:
        print("\n" + "-"*80)
        print("5️⃣  COMPLIANCE RESULTS")
        print("-"*80)
        
        # NIST AI RMF
        nist_ai_rmf = context.compliance_results.get("nist_ai_rmf", {})
        nist_passed = sum(1 for s in nist_ai_rmf.values() if s == "pass")
        print(f"   NIST AI RMF: {nist_passed}/{len(nist_ai_rmf)} characteristics PASS")
        
        # CMMC Level 2
        cmmc_l2 = context.compliance_results.get("cmmc_l2", {})
        cmmc_passed = sum(1 for s in cmmc_l2.values() if s == "pass")
        print(f"   CMMC Level 2: {cmmc_passed}/{len(cmmc_l2)} controls PASS")
        
        # NIST 800-53
        nist_800_53 = context.compliance_results.get("nist_800_53", {})
        nist_800_53_passed = sum(1 for s in nist_800_53.values() if s == "pass")
        print(f"   NIST 800-53: {nist_800_53_passed}/{len(nist_800_53)} controls PASS")
        
        # OSCAL
        oscal = context.compliance_results.get("oscal_document")
        if oscal:
            findings_count = len(oscal.get("assessment-results", {}).get("results", [{}])[0].get("findings", []))
            print(f"   OSCAL Document: {findings_count} findings")
    
    # Final recommendation
    print("\n" + "="*80)
    print("FINAL RECOMMENDATION")
    print("="*80)
    
    if context.is_complete:
        validation_status = context.validation_results.get("overall_status", "unknown")
        
        if validation_status == "pass":
            print("\n✅ DEPLOYMENT APPROVED")
            print("   Agent passed all quality gates and compliance requirements.")
            print("   Ready for production deployment.")
        elif validation_status == "warning":
            print("\n⚠️  DEPLOYMENT WITH CAUTION")
            print("   Agent has warnings that should be reviewed.")
            print("   Consider addressing issues before production deployment.")
        else:
            print("\n🚫 DEPLOYMENT BLOCKED")
            print("   Agent failed critical quality gates.")
            print("   Must address blocking issues before deployment.")
            
            # Show recommendations
            recommendations = context.validation_results.get("recommendations", [])
            if recommendations:
                print("\n   💡 Recommendations:")
                for rec in recommendations[:5]:  # Show top 5
                    print(f"      • {rec}")
    else:
        print("\n❌ EVALUATION INCOMPLETE")
        print("   Evaluation did not complete successfully.")
        print(f"   Completed {len(context.completed_phases)}/5 phases")
    
    print("\n" + "="*80)
    print("📋 Federal Compliance:")
    print("   - CM-3: Configuration Change Control")
    print("   - SA-11: Developer Security Testing and Evaluation")
    print("="*80)
    
    return context


if __name__ == "__main__":
    result = asyncio.run(main())
    
    # Exit with appropriate code
    import sys
    if result.is_complete and result.validation_results.get("overall_status") == "pass":
        sys.exit(0)
    else:
        sys.exit(1)
