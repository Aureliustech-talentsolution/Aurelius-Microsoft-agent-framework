"""
Performance and Scalability Tests for MLTE Integration

Tests evaluation performance, throughput, and resource usage.

Federal Compliance: SA-11 (Developer Testing)
"""

import pytest
import time
from pathlib import Path
from mlte_integration import MLTEOrchestrator


@pytest.fixture
def minimal_agent_spec():
    """Minimal agent spec for performance tests."""
    return {
        "name": "PerfTestAgent",
        "description": "Agent for performance testing",
        "model_id": "gpt-3.5-turbo",
        "category": "Public",
        "capabilities": ["basic_capability"],
    }


@pytest.mark.asyncio
@pytest.mark.performance
class TestEvaluationPerformance:
    """Test MLTE evaluation performance."""
    
    async def test_evaluation_latency(self, minimal_agent_spec, tmp_path):
        """Test single evaluation latency."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=False,  # Faster for latency test
        )
        
        start_time = time.time()
        context = await orchestrator.evaluate_agent(minimal_agent_spec)
        end_time = time.time()
        
        duration = end_time - start_time
        
        # Performance assertion (should complete reasonably fast)
        # Adjust threshold based on actual system performance
        assert duration < 300  # 5 minutes max for basic evaluation
        
        print(f"\n⏱️  Evaluation latency: {duration:.2f}s")
        print(f"   Completed phases: {len(context.completed_phases)}")
        print(f"   Errors: {len(context.errors)}")
    
    async def test_throughput_sequential(self, minimal_agent_spec, tmp_path):
        """Test sequential evaluation throughput."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=False,
        )
        
        num_evaluations = 3
        start_time = time.time()
        
        contexts = []
        for i in range(num_evaluations):
            spec = minimal_agent_spec.copy()
            spec["name"] = f"PerfTestAgent_{i}"
            context = await orchestrator.evaluate_agent(spec)
            contexts.append(context)
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = num_evaluations / duration
        
        print(f"\n📊 Sequential throughput:")
        print(f"   Evaluations: {num_evaluations}")
        print(f"   Total time: {duration:.2f}s")
        print(f"   Throughput: {throughput:.2f} evaluations/second")
        print(f"   Avg latency: {duration/num_evaluations:.2f}s/evaluation")
        
        assert len(contexts) == num_evaluations
    
    async def test_phase_timing(self, minimal_agent_spec, tmp_path):
        """Test timing of individual phases."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,  # Test all phases
        )
        
        context = await orchestrator.evaluate_agent(minimal_agent_spec)
        
        print(f"\n⏱️  Phase timing:")
        print(f"   Total duration: {context.duration_seconds:.2f}s")
        print(f"   Completed phases: {len(context.completed_phases)}")
        
        # Each phase should complete reasonably fast
        assert context.duration_seconds < 300


@pytest.mark.asyncio
@pytest.mark.performance
class TestScalability:
    """Test scalability with complex agents."""
    
    async def test_complex_agent_evaluation(self, tmp_path):
        """Test evaluation of complex agent with many capabilities."""
        complex_spec = {
            "name": "ComplexMultiCapabilityAgent",
            "description": "Complex agent with multiple capabilities for scalability testing",
            "model_id": "gpt-4",
            "version": "1.0.0",
            "category": "CUI",
            "capabilities": [
                "nlp_understanding",
                "data_analysis",
                "code_generation",
                "image_processing",
                "api_integration",
                "database_queries",
                "report_generation",
                "user_interaction",
            ],
            "deployment_env": "production",
            "data_classification": "confidential",
        }
        
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        start_time = time.time()
        context = await orchestrator.evaluate_agent(complex_spec)
        duration = time.time() - start_time
        
        print(f"\n🔄 Complex agent evaluation:")
        print(f"   Capabilities: {len(complex_spec['capabilities'])}")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Completed phases: {len(context.completed_phases)}")
        
        # Should handle complexity
        assert context is not None


@pytest.mark.asyncio
@pytest.mark.performance
class TestResourceUsage:
    """Test resource usage patterns."""
    
    async def test_output_directory_size(self, minimal_agent_spec, tmp_path):
        """Test output directory size after evaluation."""
        orchestrator = MLTEOrchestrator(
            output_dir=tmp_path,
            enable_compliance=True,
        )
        
        context = await orchestrator.evaluate_agent(minimal_agent_spec)
        
        # Calculate total output size
        total_size = sum(
            f.stat().st_size
            for f in tmp_path.rglob("*")
            if f.is_file()
        )
        
        total_size_mb = total_size / (1024 * 1024)
        
        print(f"\n💾 Resource usage:")
        print(f"   Output size: {total_size_mb:.2f} MB")
        print(f"   Files created: {len(list(tmp_path.rglob('*')))}")
        
        # Sanity check on output size
        assert total_size_mb < 100  # Should be reasonable


# Federal Compliance Annotation
pytest.mark.federal_compliance = {
    "SA-11": "Developer Security Testing and Evaluation",
}
