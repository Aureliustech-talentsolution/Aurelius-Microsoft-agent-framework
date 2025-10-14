"""Tests for NegotiationAgent."""

import pytest
from mlte_integration.agents.negotiation import NegotiationAgent


class TestNegotiationAgent:
    """Tests for NegotiationAgent."""
    
    @pytest.mark.asyncio
    async def test_generate_qas(self):
        """Test QAS generation."""
        agent = NegotiationAgent(llm_client=None)
        
        spec = {
            "name": "TestAgent",
            "agent_type": "ChatAgent",
            "instructions": "Be helpful",
            "tools": ["search"]
        }
        
        qas = await agent.generate_qas(spec)
        
        assert "properties" in qas
        assert "accuracy_metrics" in qas
        assert "performance_requirements" in qas
        assert "safety_constraints" in qas
