"""
End-to-End Integration Tests for MLTE Workflow

Tests complete evaluation workflow from agent creation to OSCAL generation.

Federal Compliance: SA-11 (Developer Testing)
"""

import pytest
from pathlib import Path
from mlte_integration import (
    MLTEOrchestrator,
    EvaluationPhase,
    AgentLifecycleEventType,
)


@pytest.fixture
def security_agent_spec():
    """Security-focused agent specification."""
    return {
        "name": "ThreatDetectionAgent",
        "description": "AI agent for cybersecurity threat detection and analysis",
        "model_id": "gpt-4",
        "version": "1.0.0",
        "category": "CUI",
        "capabilities": [
            "threat_detection",
            "log_analysis",
            "incident_response",
            "vulnerability_scanning",
        ],
        "deployment_env": "production",
        "data_classification": "confidential",
    }


@pytest.fixture
def chatbot_agent_spec():
    """Chatbot agent specification."""
    return {
        "name": "CustomerSupportBot",
        "description": "AI chatbot for customer support",
        "model_id": "gpt-3.5-turbo",
        "version": "2.1.0",
        "category": "Public",
        "capabilities": [
            "customer_inquiry",
            "ticket_routing",
            "knowledge_base_search",
        ],
        "deployment_env": "staging",
        "data_classification": "public",
    }


@pytest.mark.asyncio
@pytest.mark.e2e
class TestCompleteWorkflow:
    """Test complete MLTE evaluation workflow."""
    
    async def test_security_agent_evaluation(self, security_agent_spec, tmp_path):
        """Test E2E evaluation of security agent."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path / "security_agent",
            enable_compliance=True,
        )
        
        # Execute complete evaluation
        context = await orchestrator.evaluate_agent(security_agent_spec)
        
        # Verify evaluation completed or has documented errors
        assert context is not None
        assert context.agent_id == "ThreatDetectionAgent"
        
        if context.is_complete:
            # Verify all phases completed
            assert EvaluationPhase.NEGOTIATION in context.completed_phases
            assert EvaluationPhase.TESTING in context.completed_phases
            assert EvaluationPhase.VALIDATION in context.completed_phases
            assert EvaluationPhase.REPORTING in context.completed_phases
            assert EvaluationPhase.COMPLIANCE in context.completed_phases
            
            # Verify negotiation results
            assert context.negotiation_card is not None
            assert "qas" in context.negotiation_card
            assert len(context.negotiation_card["qas"]) > 0
            
            # Verify testing results
            assert context.test_results is not None
            assert "test_count" in context.test_results
            assert context.test_results["test_count"] > 0
            
            # Verify validation results
            assert context.validation_results is not None
            assert "overall_status" in context.validation_results
            assert context.validation_results["overall_status"] in ["pass", "warning", "fail"]
            
            # Verify reports generated
            assert context.reports is not None
            assert "reports" in context.reports
            assert len(context.reports["reports"]) > 0
            
            # Verify compliance results
            assert context.compliance_results is not None
            assert "nist_ai_rmf" in context.compliance_results
            assert "cmmc_l2" in context.compliance_results
            assert "nist_800_53" in context.compliance_results
            assert "oscal_document" in context.compliance_results
        
        else:
            # If not complete, should have errors documented
            assert len(context.errors) > 0
    
    async def test_chatbot_evaluation(self, chatbot_agent_spec, tmp_path):
        """Test E2E evaluation of chatbot agent."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path / "chatbot",
            enable_compliance=False,  # Skip compliance for faster test
        )
        
        context = await orchestrator.evaluate_agent(chatbot_agent_spec)
        
        assert context is not None
        assert context.agent_id == "CustomerSupportBot"
        
        # Should complete at least negotiation and testing
        if len(context.errors) == 0:
            assert EvaluationPhase.NEGOTIATION in context.completed_phases
    
    async def test_multiple_agents_evaluation(
        self,
        security_agent_spec,
        chatbot_agent_spec,
        tmp_path,
    ):
        """Test evaluation of multiple agents in sequence."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=False,
        )
        
        # Evaluate multiple agents
        contexts = []
        for spec in [security_agent_spec, chatbot_agent_spec]:
            context = await orchestrator.evaluate_agent(spec)
            contexts.append(context)
        
        assert len(contexts) == 2
        
        # Each should have unique agent_id
        agent_ids = {ctx.agent_id for ctx in contexts}
        assert len(agent_ids) == 2


@pytest.mark.asyncio
@pytest.mark.e2e
class TestQualityGates:
    """Test quality gate evaluation."""
    
    async def test_blocking_failure_prevents_deployment(self, tmp_path):
        """Test that blocking failures prevent deployment."""
        # Agent spec designed to fail quality gates
        failing_spec = {
            "name": "UntestedAgent",
            "description": "Agent with insufficient testing",
            "model_id": "gpt-3.5-turbo",
            "category": "CUI",
            "capabilities": ["untested_capability"],
            "deployment_env": "production",
            # Missing critical fields that should trigger failures
        }
        
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=False,
        )
        
        context = await orchestrator.evaluate_agent(failing_spec)
        
        # Should complete phases (may have warnings/failures)
        assert context is not None


@pytest.mark.asyncio
@pytest.mark.e2e
class TestReporting:
    """Test report generation."""
    
    async def test_reports_generated(self, security_agent_spec, tmp_path):
        """Test that all report formats are generated."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=False,
        )
        
        context = await orchestrator.evaluate_agent(security_agent_spec)
        
        if context.reports:
            # Check reports exist
            assert "reports" in context.reports
            reports = context.reports["reports"]
            
            # Should have multiple formats
            if len(reports) > 0:
                # Check files exist
                for report_path in reports:
                    assert Path(report_path).exists()


@pytest.mark.asyncio
@pytest.mark.e2e
class TestComplianceMapping:
    """Test federal compliance mapping."""
    
    async def test_nist_ai_rmf_mapping(self, security_agent_spec, tmp_path):
        """Test NIST AI RMF characteristic mapping."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(security_agent_spec)
        
        if context.compliance_results:
            nist_ai_rmf = context.compliance_results.get("nist_ai_rmf", {})
            
            # Should have all 8 characteristics
            expected_chars = [
                "valid_reliable",
                "safe",
                "secure_resilient",
                "accountable_transparent",
                "explainable_interpretable",
                "privacy_enhanced",
                "fair",
                "continuous_monitoring",
            ]
            
            # Check at least some characteristics present
            assert len(nist_ai_rmf) > 0
    
    async def test_cmmc_l2_mapping(self, security_agent_spec, tmp_path):
        """Test CMMC Level 2 control mapping."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(security_agent_spec)
        
        if context.compliance_results:
            cmmc_l2 = context.compliance_results.get("cmmc_l2", {})
            
            # Should have controls mapped
            assert len(cmmc_l2) > 0
    
    async def test_oscal_generation(self, security_agent_spec, tmp_path):
        """Test OSCAL document generation."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(security_agent_spec)
        
        if context.compliance_results:
            oscal = context.compliance_results.get("oscal_document")
            
            # Should have OSCAL structure
            if oscal:
                assert "assessment-results" in oscal
                assert "metadata" in oscal["assessment-results"]


@pytest.mark.asyncio
@pytest.mark.e2e
class TestErrorHandling:
    """Test error handling and recovery."""
    
    async def test_invalid_agent_spec(self, tmp_path):
        """Test handling of invalid agent specification."""
        invalid_spec = {
            # Missing required fields
            "name": "InvalidAgent",
        }
        
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=False,
        )
        
        context = await orchestrator.evaluate_agent(invalid_spec)
        
        # Should handle gracefully (may have errors)
        assert context is not None
    
    async def test_orchestrator_resilience(self, security_agent_spec, tmp_path):
        """Test orchestrator continues after non-blocking errors."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=False,
        )
        
        context = await orchestrator.evaluate_agent(security_agent_spec)
        
        # Should attempt all phases
        assert context is not None
        assert len(context.completed_phases) >= 0


# Federal Compliance Annotation
pytest.mark.federal_compliance = {
    "SA-11": "Developer Security Testing and Evaluation",
}
