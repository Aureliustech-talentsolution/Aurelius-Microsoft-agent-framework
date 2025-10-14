"""Example: Using NegotiationAgent to generate QAS."""

from mlte_integration.agents.negotiation import NegotiationAgent


async def main():
    """Demonstrate NegotiationAgent usage."""
    agent = NegotiationAgent(llm_client=None)
    
    spec = {
        "name": "CustomerServiceAgent",
        "agent_type": "ChatAgent",
        "instructions": "Help customers with their questions",
        "tools": ["search", "email"]
    }
    
    qas = await agent.generate_qas(spec)
    
    print("Generated QAS:")
    print(f"  Properties: {len(qas['properties'])}")
    print(f"  Accuracy Metrics: {len(qas['accuracy_metrics'])}")
    print(f"  Performance Requirements: {len(qas['performance_requirements'])}")
    print(f"  Safety Constraints: {len(qas['safety_constraints'])}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
