"""Tests for MLTEEvaluationMiddleware."""

import pytest
from mlte_integration.middleware.evaluation import (
    MLTEEvaluationMiddleware,
    EvaluationMode,
)


class MockOrchestrator:
    """Mock orchestrator for testing."""
    
    def __init__(self):
        self.run_count = 0
    
    async def run(self, agent_spec):
        """Mock run method."""
        self.run_count += 1
        return {"status": "completed"}


class TestMLTEEvaluationMiddleware:
    """Tests for middleware."""
    
    def test_initialization(self):
        """Test middleware initialization."""
        orchestrator = MockOrchestrator()
        middleware = MLTEEvaluationMiddleware(
            orchestrator,
            mode=EvaluationMode.ASYNCHRONOUS
        )
        
        assert middleware.orchestrator == orchestrator
        assert middleware.mode == EvaluationMode.ASYNCHRONOUS
        assert not middleware.is_running()
    
    def test_start_stop(self):
        """Test start/stop functionality."""
        middleware = MLTEEvaluationMiddleware(MockOrchestrator())
        
        middleware.start()
        assert middleware.is_running()
        
        middleware.stop()
        assert not middleware.is_running()
    
    def test_de_duplication(self):
        """Test duplicate evaluation prevention."""
        middleware = MLTEEvaluationMiddleware(MockOrchestrator())
        
        agent_id = "test-agent-1"
        middleware._evaluated_agents.add(agent_id)
        
        evaluated = middleware.get_evaluated_agents()
        assert agent_id in evaluated
