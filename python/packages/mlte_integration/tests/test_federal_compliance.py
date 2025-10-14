"""
Unit tests for FederalComplianceAgent and sub-agents.
"""

import pytest
from mlte_integration.agents.federal_compliance import (
    FederalComplianceAgent,
    ComplianceResults,
    ComplianceStatus,
)


@pytest.fixture
def sample_evaluation_results():
    """Sample evaluation results."""
    return {
        "validation_results": {
            "overall_status": "WARNING",
            "gate_results": [
                {
                    "name": "Prompt Injection Resistance",
                    "status": "FAIL",
                    "severity": "blocking",
                    "reasoning": "Below threshold",
                },
                {
                    "name": "PII Protection",
                    "status": "PASS",
                    "severity": "blocking",
                },
                {
                    "name": "Fairness Check",
                    "status": "WARNING",
                    "severity": "warning",
                },
            ],
        },
    }


@pytest.mark.asyncio
async def test_federal_compliance_agent_initialization():
    """Test FederalComplianceAgent initialization."""
    agent = FederalComplianceAgent()
    
    assert agent is not None


@pytest.mark.asyncio
async def test_map_compliance(sample_evaluation_results):
    """Test compliance mapping."""
    agent = FederalComplianceAgent()
    
    results = await agent.map_compliance(
        sample_evaluation_results,
        agent_spec={"name": "TestAgent"},
    )
    
    assert isinstance(results, ComplianceResults)
    assert results.nist_ai_rmf is not None
    assert results.cmmc_l2 is not None
    assert results.nist_800_53 is not None


@pytest.mark.asyncio
async def test_nist_ai_rmf_mapping(sample_evaluation_results):
    """Test NIST AI RMF mapping."""
    agent = FederalComplianceAgent()
    results = await agent.map_compliance(sample_evaluation_results)
    
    # Check characteristics are mapped
    assert len(results.nist_ai_rmf.characteristics) > 0
    
    # Check Secure and Resilient is FAIL (due to injection failure)
    assert results.nist_ai_rmf.characteristics.get("Secure and Resilient") == ComplianceStatus.FAIL


@pytest.mark.asyncio
async def test_cmmc_mapping(sample_evaluation_results):
    """Test CMMC L2 mapping."""
    agent = FederalComplianceAgent()
    results = await agent.map_compliance(sample_evaluation_results)
    
    # Check controls are mapped
    assert len(results.cmmc_l2.controls) > 0
    
    # Check SC-7 (Boundary Protection) is relevant
    assert "SC-7" in results.cmmc_l2.controls


@pytest.mark.asyncio
async def test_nist_800_53_mapping(sample_evaluation_results):
    """Test NIST 800-53 mapping."""
    agent = FederalComplianceAgent()
    results = await agent.map_compliance(sample_evaluation_results)
    
    # Check controls are mapped
    assert len(results.nist_800_53.controls) > 0
    
    # Check SA-11 is present
    assert "SA-11" in results.nist_800_53.controls


@pytest.mark.asyncio
async def test_oscal_generation(sample_evaluation_results):
    """Test OSCAL document generation."""
    agent = FederalComplianceAgent()
    results = await agent.map_compliance(sample_evaluation_results)
    
    assert results.oscal_document is not None
    assert "assessment-results" in results.oscal_document


def test_compliance_status_enum():
    """Test ComplianceStatus enum."""
    assert ComplianceStatus.PASS.value == "pass"
    assert ComplianceStatus.FAIL.value == "fail"
    assert ComplianceStatus.WARNING.value == "warning"
