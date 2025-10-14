"""Tests for RuntimeMonitor."""

import pytest
from datetime import datetime, timedelta
from mlte_integration.monitoring.runtime_monitor import RuntimeMonitor, RuntimeMetrics


class MockOrchestrator:
    """Mock orchestrator for testing."""
    
    def __init__(self):
        self.run_count = 0
    
    async def run(self, agent_spec, trigger_reason=None, trigger_details=None):
        """Mock run method."""
        self.run_count += 1
        return {"status": "completed"}


class TestRuntimeMetrics:
    """Tests for RuntimeMetrics."""
    
    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        metrics = RuntimeMetrics(agent_id="test-agent")
        metrics.total_runs = 100
        metrics.successful_runs = 90
        
        assert metrics.success_rate == 0.90
    
    def test_avg_latency_calculation(self):
        """Test average latency calculation."""
        metrics = RuntimeMetrics(agent_id="test-agent")
        metrics.total_runs = 10
        metrics.total_latency_ms = 5000.0
        
        assert metrics.avg_latency_ms == 500.0


class TestRuntimeMonitor:
    """Tests for RuntimeMonitor."""
    
    def test_initialization(self):
        """Test monitor initialization."""
        orchestrator = MockOrchestrator()
        monitor = RuntimeMonitor(
            orchestrator,
            success_rate_threshold=0.90,
            latency_threshold_ms=5000.0,
        )
        
        assert monitor.orchestrator == orchestrator
        assert monitor.success_rate_threshold == 0.90
        assert not monitor.is_running()
    
    def test_start_stop(self):
        """Test start/stop functionality."""
        monitor = RuntimeMonitor(MockOrchestrator())
        
        monitor.start()
        assert monitor.is_running()
        
        monitor.stop()
        assert not monitor.is_running()
    
    def test_metrics_tracking(self):
        """Test metrics collection."""
        monitor = RuntimeMonitor(MockOrchestrator())
        
        agent_id = "test-agent"
        metrics = RuntimeMetrics(agent_id=agent_id)
        metrics.total_runs = 100
        metrics.successful_runs = 95
        
        monitor._metrics[agent_id] = metrics
        
        retrieved = monitor.get_metrics(agent_id)
        assert retrieved["success_rate"] == 0.95
