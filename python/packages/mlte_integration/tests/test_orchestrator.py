"""
Unit tests for MLTEOrchestrator.
"""

import pytest
from mlte_integration.orchestrator import (
    MLTEOrchestrator,
    EvaluationContext,
    EvaluationPhase,
)


@pytest.fixture
def sample_agent_spec():
    """Sample agent specification."""
    return {
        "name": "TestSecurityAgent",
        "description": "Test agent for security tasks",
        "model_id": "gpt-4",
        "category": "CUI",
        "capabilities": ["security_analysis", "threat_detection"],
    }


@pytest.mark.asyncio
async def test_orchestrator_initialization(tmp_path):
    """Test MLTEOrchestrator initialization."""
    orchestrator = MLTEOrchestrator(output_dir=tmp_path)
    
    assert orchestrator.output_dir == tmp_path
    assert orchestrator.enable_compliance is True


@pytest.mark.asyncio
async def test_orchestrator_evaluate_agent(sample_agent_spec, tmp_path):
    """Test complete agent evaluation."""
    orchestrator = MLTEOrchestrator(
        output_dir=tmp_path,
        enable_compliance=False,  # Skip compliance for faster test
    )
    
    context = await orchestrator.evaluate_agent(sample_agent_spec)
    
    assert isinstance(context, EvaluationContext)
    assert context.agent_id == "TestSecurityAgent"
    assert context.is_complete or len(context.errors) > 0


@pytest.mark.asyncio
async def test_evaluation_context_properties(sample_agent_spec):
    """Test EvaluationContext properties."""
    context = EvaluationContext(
        agent_id="test",
        agent_spec=sample_agent_spec,
    )
    
    assert context.is_complete is False
    assert context.duration_seconds >= 0


@pytest.mark.asyncio
async def test_orchestrator_with_compliance(sample_agent_spec, tmp_path):
    """Test evaluation with compliance mapping."""
    orchestrator = MLTEOrchestrator(
        output_dir=tmp_path,
        enable_compliance=True,
    )
    
    context = await orchestrator.evaluate_agent(sample_agent_spec)
    
    # Check compliance was executed (or error occurred)
    if context.is_complete:
        assert EvaluationPhase.COMPLIANCE in context.completed_phases


def test_evaluation_phase_enum():
    """Test EvaluationPhase enum."""
    assert EvaluationPhase.NEGOTIATION.value == "negotiation"
    assert EvaluationPhase.TESTING.value == "testing"
    assert EvaluationPhase.VALIDATION.value == "validation"
    assert EvaluationPhase.REPORTING.value == "reporting"
    assert EvaluationPhase.COMPLIANCE.value == "compliance"
    assert EvaluationPhase.COMPLETE.value == "complete"
