"""Tests for TestingAgent and sub-agents."""

import pytest
from mlte_integration.agents.testing import TestingAgent, TestPlan, TestResults


class TestTestingAgent:
    """Tests for TestingAgent."""
    
    @pytest.mark.asyncio
    async def test_testing_agent_run(self):
        """Test full testing workflow."""
        agent = TestingAgent(llm_client=None)
        
        agent_spec = {
            "name": "TestAgent",
            "instructions": "Be helpful"
        }
        
        qas_list = [
            {
                "name": "Security Test",
                "quality_attribute": "Security",
                "measurement": "injection_rate < 0.05"
            }
        ]
        
        results = await agent.run(agent_spec, qas_list)
        
        assert isinstance(results, TestResults)
        assert results.total > 0
    
    def test_get_sub_agents(self):
        """Test sub-agent access."""
        agent = TestingAgent(llm_client=None)
        sub_agents = agent.get_sub_agents()
        
        assert "planner" in sub_agents
        assert "executor" in sub_agents
        assert "evidence_collector" in sub_agents
