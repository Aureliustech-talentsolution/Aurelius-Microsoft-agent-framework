"""
TestingAgent - MLTE Test Execution Coordinator

Executes MLTE measurements based on generated QAS using 3 specialized sub-agents.

Federal Compliance: SA-11 (Developer Testing)
"""

from typing import Dict, Any, List, Optional
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class TestPlan:
    """Plan for test execution."""
    measurements: List[Dict[str, Any]]
    total_tests: int
    estimated_duration_sec: float


@dataclass
class TestResults:
    """Results from test execution."""
    results: List[Dict[str, Any]]
    passed: int
    failed: int
    total: int
    duration_sec: float
    evidence_artifacts: List[Dict[str, Any]] = field(default_factory=list)


class TestingAgent:
    """
    Coordinates MLTE test execution using specialized sub-agents.
    
    Sub-Agents:
    - TestPlannerSubAgent: Maps QAS to MLTE measurements
    - TestExecutorSubAgent: Executes measurements  
    - EvidenceCollectorSubAgent: Summarizes results
    
    Federal Compliance: SA-11 (Developer Testing)
    """
    
    def __init__(self, llm_client: Any):
        """
        Initialize TestingAgent.
        
        Args:
            llm_client: LLM client for sub-agents
        """
        self.llm_client = llm_client
        
        # Initialize sub-agents
        from mlte_integration.agents.testing_subagents import (
            TestPlannerSubAgent,
            TestExecutorSubAgent,
            EvidenceCollectorSubAgent,
        )
        
        self.planner = TestPlannerSubAgent(llm_client)
        self.executor = TestExecutorSubAgent(llm_client)
        self.evidence_collector = EvidenceCollectorSubAgent(llm_client)
        
        logger.info("TestingAgent initialized with 3 sub-agents")
    
    async def run(
        self,
        agent_spec: Dict[str, Any],
        qas_list: List[Dict[str, Any]],
    ) -> TestResults:
        """
        Execute MLTE tests for agent.
        
        Args:
            agent_spec: Agent specification
            qas_list: List of Quality Attribute Scenarios from NegotiationAgent
        
        Returns:
            TestResults with evidence artifacts
        
        Federal Compliance: SA-11
        """
        logger.info(
            f"Starting MLTE testing for agent: {agent_spec.get('name')}",
            extra={"qas_count": len(qas_list)}
        )
        
        # Phase 1: Plan tests
        logger.info("Phase 1: Planning tests (TestPlannerSubAgent)")
        test_plan = await self.planner.generate_plan(qas_list, agent_spec)
        
        logger.info(
            f"Test plan generated: {test_plan.total_tests} tests",
            extra={"estimated_duration": test_plan.estimated_duration_sec}
        )
        
        # Phase 2: Execute tests
        logger.info("Phase 2: Executing tests (TestExecutorSubAgent)")
        test_results = await self.executor.execute_plan(test_plan, agent_spec)
        
        logger.info(
            f"Tests completed: {test_results.passed}/{test_results.total} passed",
            extra={"duration": test_results.duration_sec}
        )
        
        # Phase 3: Collect evidence
        logger.info("Phase 3: Collecting evidence (EvidenceCollectorSubAgent)")
        evidence = await self.evidence_collector.summarize_results(test_results)
        
        logger.info(f"Evidence collected: {len(evidence)} artifacts")
        
        # Attach evidence to results
        test_results.evidence_artifacts = evidence
        
        return test_results
    
    def get_sub_agents(self) -> Dict[str, Any]:
        """
        Get sub-agent instances.
        
        Returns:
            Dictionary of sub-agents
        """
        return {
            "planner": self.planner,
            "executor": self.executor,
            "evidence_collector": self.evidence_collector,
        }
