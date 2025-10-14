"""
Example Scenarios - Complete MLTE Evaluation Workflows

Demonstrates evaluation of various agent types:
1. Security-focused agent (threat detection)
2. Customer service chatbot
3. Data analyst agent

Federal Compliance: CM-3 (Configuration Management), SA-11 (Developer Testing)
"""

import asyncio
from pathlib import Path
from mlte_integration import MLTEOrchestrator


async def scenario_1_security_agent():
    """Scenario 1: Evaluate security-focused threat detection agent."""
    print("\n" + "="*80)
    print("SCENARIO 1: Security-Focused Threat Detection Agent")
    print("="*80)
    
    agent_spec = {
        "name": "ThreatHunterAgent",
        "description": "Advanced threat detection and hunting agent for SOC operations",
        "model_id": "gpt-4",
        "version": "1.2.0",
        "category": "CUI",
        "capabilities": [
            "threat_detection",
            "log_analysis",
            "incident_triage",
            "ioc_extraction",
            "threat_intelligence",
            "attack_pattern_matching",
        ],
        "deployment_env": "production",
        "data_classification": "cui",
        "compliance_requirements": ["NIST_800_53", "CMMC_L2"],
    }
    
    print(f"\nAgent: {agent_spec['name']}")
    print(f"Purpose: {agent_spec['description']}")
    print(f"Category: {agent_spec['category']}")
    print(f"Capabilities: {len(agent_spec['capabilities'])}")
    
    # Initialize orchestrator with compliance
    output_dir = Path("mlte_examples/security_agent")
    orchestrator = MLTEOrchestrator(
        output_dir=output_dir,
        enable_compliance=True,  # Critical for CUI handling
    )
    
    print(f"\n🚀 Starting MLTE evaluation...")
    
    # Execute evaluation
    context = await orchestrator.evaluate_agent(agent_spec)
    
    # Display results
    print(f"\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)
    print(f"Status: {'✅ COMPLETE' if context.is_complete else '⚠️ INCOMPLETE'}")
    print(f"Duration: {context.duration_seconds:.2f}s")
    print(f"Phases: {len(context.completed_phases)}/5")
    
    if context.validation_results:
        status = context.validation_results.get("overall_status", "unknown").upper()
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"\nValidation: {status_icon} {status}")
    
    if context.compliance_results:
        print(f"\n🔒 Compliance Results:")
        nist_ai_rmf = context.compliance_results.get("nist_ai_rmf", {})
        cmmc_l2 = context.compliance_results.get("cmmc_l2", {})
        print(f"   NIST AI RMF: {sum(1 for s in nist_ai_rmf.values() if s == 'pass')}/{len(nist_ai_rmf)} PASS")
        print(f"   CMMC L2: {sum(1 for s in cmmc_l2.values() if s == 'pass')}/{len(cmmc_l2)} PASS")
    
    print(f"\n📂 Reports: {output_dir}")
    return context


async def scenario_2_customer_chatbot():
    """Scenario 2: Evaluate customer service chatbot."""
    print("\n" + "="*80)
    print("SCENARIO 2: Customer Service Chatbot")
    print("="*80)
    
    agent_spec = {
        "name": "SupportBot3000",
        "description": "AI-powered customer support chatbot for e-commerce",
        "model_id": "gpt-3.5-turbo",
        "version": "3.0.1",
        "category": "Public",
        "capabilities": [
            "customer_inquiry_handling",
            "order_status_lookup",
            "product_recommendations",
            "return_processing",
            "basic_troubleshooting",
        ],
        "deployment_env": "production",
        "data_classification": "public",
        "performance_targets": {
            "response_time_ms": 2000,
            "accuracy": 0.85,
            "customer_satisfaction": 4.0,
        },
    }
    
    print(f"\nAgent: {agent_spec['name']}")
    print(f"Purpose: {agent_spec['description']}")
    print(f"Category: {agent_spec['category']}")
    print(f"Target Response Time: {agent_spec['performance_targets']['response_time_ms']}ms")
    
    # Initialize orchestrator (no compliance for public-facing bot)
    output_dir = Path("mlte_examples/chatbot")
    orchestrator = MLTEOrchestrator(
        output_dir=output_dir,
        enable_compliance=False,
    )
    
    print(f"\n🚀 Starting MLTE evaluation...")
    
    # Execute evaluation
    context = await orchestrator.evaluate_agent(agent_spec)
    
    # Display results
    print(f"\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)
    print(f"Status: {'✅ COMPLETE' if context.is_complete else '⚠️ INCOMPLETE'}")
    print(f"Duration: {context.duration_seconds:.2f}s")
    
    if context.validation_results:
        gate_results = context.validation_results.get("gate_results", [])
        passed = sum(1 for g in gate_results if g.get("status") == "pass")
        print(f"\nQuality Gates: {passed}/{len(gate_results)} PASSED")
    
    if context.reports:
        reports = context.reports.get("reports", [])
        print(f"\n📊 Reports Generated: {len(reports)}")
    
    print(f"\n📂 Reports: {output_dir}")
    return context


async def scenario_3_data_analyst():
    """Scenario 3: Evaluate data analyst agent."""
    print("\n" + "="*80)
    print("SCENARIO 3: Data Analyst Agent")
    print("="*80)
    
    agent_spec = {
        "name": "DataInsightsAgent",
        "description": "AI agent for data analysis, visualization, and insights generation",
        "model_id": "gpt-4",
        "version": "2.0.0",
        "category": "Internal",
        "capabilities": [
            "sql_query_generation",
            "data_visualization",
            "statistical_analysis",
            "trend_detection",
            "report_generation",
            "predictive_modeling",
        ],
        "deployment_env": "staging",
        "data_classification": "internal",
        "data_sources": ["sql_database", "csv_files", "api_endpoints"],
    }
    
    print(f"\nAgent: {agent_spec['name']}")
    print(f"Purpose: {agent_spec['description']}")
    print(f"Category: {agent_spec['category']}")
    print(f"Data Sources: {', '.join(agent_spec['data_sources'])}")
    
    # Initialize orchestrator
    output_dir = Path("mlte_examples/data_analyst")
    orchestrator = MLTEOrchestrator(
        output_dir=output_dir,
        enable_compliance=True,  # Internal data requires compliance
    )
    
    print(f"\n🚀 Starting MLTE evaluation...")
    
    # Execute evaluation
    context = await orchestrator.evaluate_agent(agent_spec)
    
    # Display results
    print(f"\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)
    print(f"Status: {'✅ COMPLETE' if context.is_complete else '⚠️ INCOMPLETE'}")
    print(f"Duration: {context.duration_seconds:.2f}s")
    print(f"Phases: {len(context.completed_phases)}/5")
    
    if context.validation_results:
        recommendations = context.validation_results.get("recommendations", [])
        if recommendations:
            print(f"\n💡 Recommendations ({len(recommendations)}):")
            for rec in recommendations[:3]:
                print(f"   • {rec}")
    
    print(f"\n📂 Reports: {output_dir}")
    return context


async def main():
    """Run all example scenarios."""
    print("\n" + "="*80)
    print("MLTE EVALUATION - EXAMPLE SCENARIOS")
    print("="*80)
    print("\nThis demonstration shows complete MLTE evaluation for 3 agent types:")
    print("  1. Security-focused threat detection agent (CUI)")
    print("  2. Customer service chatbot (Public)")
    print("  3. Data analyst agent (Internal)")
    print("\nEach evaluation includes:")
    print("  • QAS generation (Negotiation)")
    print("  • MLTE measurements (Testing)")
    print("  • Quality gate evaluation (Validation)")
    print("  • Multi-format reports (Reporting)")
    print("  • Federal compliance mapping (Compliance)")
    
    # Run scenarios
    try:
        context1 = await scenario_1_security_agent()
        await asyncio.sleep(1)  # Brief pause between scenarios
        
        context2 = await scenario_2_customer_chatbot()
        await asyncio.sleep(1)
        
        context3 = await scenario_3_data_analyst()
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        contexts = [context1, context2, context3]
        completed = sum(1 for c in contexts if c.is_complete)
        
        print(f"\nScenarios completed: {completed}/3")
        
        for i, context in enumerate(contexts, 1):
            status = "✅ COMPLETE" if context.is_complete else "⚠️ INCOMPLETE"
            print(f"  {i}. {context.agent_id}: {status}")
        
        print("\n📂 All reports saved to: mlte_examples/")
        print("\n" + "="*80)
        print("💡 Tip: Review the generated reports for detailed results!")
        print("="*80)
    
    except Exception as e:
        print(f"\n❌ Error running scenarios: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
