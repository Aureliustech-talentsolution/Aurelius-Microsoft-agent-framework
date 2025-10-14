"""Example: Using TestingAgent with sub-agents."""

from mlte_integration.agents.testing import TestingAgent


async def main():
    """Demonstrate TestingAgent usage."""
    agent = TestingAgent(llm_client=None)
    
    agent_spec = {
        "name": "CustomerServiceAgent",
        "instructions": "Help customers with questions"
    }
    
    qas_list = [
        {
            "name": "Prompt Injection Resistance",
            "quality_attribute": "Security",
            "priority": "Critical",
            "measurement": "injection_rate < 0.05"
        },
        {
            "name": "Response Latency",
            "quality_attribute": "Performance",
            "priority": "High",
            "measurement": "latency_ms < 2000"
        }
    ]
    
    print("Running MLTE tests...")
    results = await agent.run(agent_spec, qas_list)
    
    print(f"\nResults: {results.passed}/{results.total} passed")
    print(f"Duration: {results.duration_sec:.2f}s")
    print(f"Evidence artifacts: {len(results.evidence_artifacts)}")
    
    for evidence in results.evidence_artifacts:
        print(f"\n- {evidence['measurement']}")
        print(f"  Finding: {evidence['finding']}")
        print(f"  Severity: {evidence['severity']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
