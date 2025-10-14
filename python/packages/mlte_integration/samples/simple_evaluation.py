"""
Simple agent evaluation example.

This sample demonstrates basic MLTE evaluation of a ChatAgent.

Usage:
    python samples/simple_evaluation.py

Federal Compliance:
- CA-2: Security assessments
"""

import asyncio
import os

# TODO: Import once agent framework is available
# from agent_framework import ChatAgent
# from agent_framework.openai import OpenAIChatClient
# from azure.identity import DefaultAzureCredential

from agent_framework_mlte_integration import MLTEOrchestratorAgent
from agent_framework_mlte_integration.config import MLTEConfig
from agent_framework_mlte_integration.types import AgentSpec


async def main():
    """Run simple agent evaluation."""
    print("=" * 60)
    print("MLTE Simple Agent Evaluation Example")
    print("=" * 60)

    # TODO: Create agent once agent framework is available
    # credential = DefaultAzureCredential()
    # chat_client = OpenAIChatClient(credential=credential)
    # agent = ChatAgent(
    #     chat_client=chat_client,
    #     name="WeatherAgent",
    #     instructions="You are a helpful weather assistant.",
    # )

    # Create agent specification
    agent_spec = AgentSpec(
        model_id="WeatherAgent",
        version="v1.0.0",
        name="Weather Assistant Agent",
        description="Provides weather information and forecasts",
        instructions="You are a helpful weather assistant.",
        tools=[],
        agent_type="ChatAgent",
        metadata={"domain": "weather", "classification": "Public"},
    )

    print(f"\nEvaluating agent: {agent_spec.name}")
    print(f"Model ID: {agent_spec.model_id}")
    print(f"Version: {agent_spec.version}")

    # Load MLTE configuration
    config = MLTEConfig.load()
    print(f"\nMLTE Store: {config.store.uri}")
    print(f"Federal Compliance: {config.federal_compliance.enabled}")

    # Create MLTE orchestrator
    # TODO: Use real chat client once available
    # orchestrator = MLTEOrchestratorAgent(
    #     chat_client=chat_client,
    #     config=config,
    #     enable_federal_compliance=True,
    # )

    print("\nStarting MLTE evaluation...")
    print("(Implementation pending - orchestrator needs chat client)")

    # TODO: Run evaluation once orchestrator is complete
    # report = await orchestrator.run(agent_spec=agent_spec)
    #
    # print("\nEvaluation Complete!")
    # print(f"Status: {report.status.value}")
    # print(f"Summary: {report.summary}")
    #
    # if report.gate_result:
    #     print(f"\nQuality Gates:")
    #     print(f"  Passed: {len(report.gate_result.passed)}")
    #     print(f"  Failed: {len(report.gate_result.failed)}")
    #     print(f"  Deployment Allowed: {report.gate_result.deployment_allowed}")
    #
    # if report.compliance_report:
    #     print(f"\nFederal Compliance:")
    #     nist_count = len(report.compliance_report.get("nist_ai_rmf", {}))
    #     cmmc_count = len(report.compliance_report.get("cmmc_controls", {}))
    #     print(f"  NIST AI RMF Characteristics: {nist_count}")
    #     print(f"  CMMC Controls: {cmmc_count}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
