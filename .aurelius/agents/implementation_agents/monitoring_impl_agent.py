"""
MonitoringImplAgent - Full Implementation

Implements RuntimeMonitor that tracks agent performance metrics
and triggers re-evaluation when thresholds are violated.

Continuous monitoring with configurable thresholds.
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class MonitoringImplAgent:
    """Autonomous agent that implements RuntimeMonitor."""

    def __init__(self):
        self.name = "MonitoringImplAgent"
        self.workspace_root = Path("d:/AI_Dev/new_microsoft-agent-framework/Microsoft-agent-framework")
        self.files_created: List[Path] = []
        logger.info(f"{self.name} initialized")

    async def run(self) -> Dict[str, Any]:
        """Execute the implementation."""
        logger.info(f"{self.name} starting full implementation")

        try:
            # Create monitor file
            await self._create_monitor()

            # Create metrics file
            await self._create_metrics()

            # Create tests
            await self._create_tests()

            # Create examples
            await self._create_examples()

            logger.info(f"{self.name} completed - {len(self.files_created)} files created")

            return {
                "status": "completed",
                "files_created": [str(f) for f in self.files_created],
            }
        except Exception:
            logger.error(f"{self.name} failed", exc_info=True)
            raise

    async def _create_monitor(self) -> None:
        """Create RuntimeMonitor."""
        file_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "mlte_integration"
            / "monitoring"
            / "runtime_monitor.py"
        )

        content = '''"""
RuntimeMonitor - Continuous Performance Monitoring

Monitors agent runtime metrics and triggers re-evaluation when
performance degrades below acceptable thresholds.

Federal Compliance: CA-8 (Continuous Monitoring)
"""

from typing import Dict, Any, Optional
import logging
import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class RuntimeMetrics:
    """Runtime performance metrics for an agent."""
    agent_id: str
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    total_latency_ms: float = 0.0
    last_evaluation: Optional[datetime] = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_runs == 0:
            return 1.0
        return self.successful_runs / self.total_runs

    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency."""
        if self.total_runs == 0:
            return 0.0
        return self.total_latency_ms / self.total_runs


class RuntimeMonitor:
    """
    Monitors agent runtime performance and triggers re-evaluation.

    Tracks:
    - Success rate
    - Latency
    - Error rate

    Triggers re-evaluation when:
    - Success rate drops below threshold
    - Latency exceeds threshold
    - Periodic interval reached

    Federal Compliance: CA-8
    """

    def __init__(
        self,
        orchestrator: Any,  # MLTEOrchestratorAgent
        success_rate_threshold: float = 0.90,
        latency_threshold_ms: float = 5000.0,
        re_evaluation_interval_hours: int = 24,
    ):
        """
        Initialize monitor.

        Args:
            orchestrator: MLTEOrchestratorAgent instance
            success_rate_threshold: Minimum acceptable success rate (0-1)
            latency_threshold_ms: Maximum acceptable latency in milliseconds
            re_evaluation_interval_hours: Hours between periodic re-evaluations
        """
        self.orchestrator = orchestrator
        self.success_rate_threshold = success_rate_threshold
        self.latency_threshold_ms = latency_threshold_ms
        self.re_evaluation_interval = timedelta(hours=re_evaluation_interval_hours)

        self._metrics: Dict[str, RuntimeMetrics] = {}
        self._running = False

        logger.info(
            "RuntimeMonitor initialized",
            extra={
                "success_rate_threshold": success_rate_threshold,
                "latency_threshold_ms": latency_threshold_ms,
                "re_evaluation_interval_hours": re_evaluation_interval_hours,
            }
        )

    def start(self) -> None:
        """
        Start monitoring runtime events.

        Registers listeners for RUN_COMPLETED and RUN_FAILED events.
        """
        if self._running:
            logger.warning("Monitor already running")
            return

        from agent_framework._events import (
            register_lifecycle_listener,
            AgentLifecycleEventType,
        )

        register_lifecycle_listener(
            AgentLifecycleEventType.RUN_COMPLETED,
            self._on_run_completed
        )

        register_lifecycle_listener(
            AgentLifecycleEventType.RUN_FAILED,
            self._on_run_failed
        )

        self._running = True
        logger.info("RuntimeMonitor started")

    def stop(self) -> None:
        """Stop monitoring."""
        self._running = False
        logger.info("RuntimeMonitor stopped")

    async def _on_run_completed(self, event: Any) -> None:
        """
        Handle RUN_COMPLETED event.

        Args:
            event: AgentLifecycleEvent
        """
        agent_id = event.agent_id
        latency_ms = event.metadata.get('latency_ms', 0.0)

        # Get or create metrics
        if agent_id not in self._metrics:
            self._metrics[agent_id] = RuntimeMetrics(agent_id=agent_id)

        metrics = self._metrics[agent_id]

        # Update metrics
        metrics.total_runs += 1
        metrics.successful_runs += 1
        metrics.total_latency_ms += latency_ms

        logger.info(
            f"Run completed: {agent_id}",
            extra={
                "success_rate": metrics.success_rate,
                "avg_latency_ms": metrics.avg_latency_ms,
            }
        )

        # Check re-evaluation triggers
        await self._check_re_evaluation_triggers(agent_id, metrics, event)

    async def _on_run_failed(self, event: Any) -> None:
        """
        Handle RUN_FAILED event.

        Args:
            event: AgentLifecycleEvent
        """
        agent_id = event.agent_id

        # Get or create metrics
        if agent_id not in self._metrics:
            self._metrics[agent_id] = RuntimeMetrics(agent_id=agent_id)

        metrics = self._metrics[agent_id]

        # Update metrics
        metrics.total_runs += 1
        metrics.failed_runs += 1

        logger.warning(
            f"Run failed: {agent_id}",
            extra={
                "success_rate": metrics.success_rate,
                "error": event.metadata.get('error'),
            }
        )

        # Check re-evaluation triggers
        await self._check_re_evaluation_triggers(agent_id, metrics, event)

    async def _check_re_evaluation_triggers(
        self,
        agent_id: str,
        metrics: RuntimeMetrics,
        event: Any,
    ) -> None:
        """
        Check if re-evaluation should be triggered.

        Args:
            agent_id: Agent identifier
            metrics: Current metrics
            event: Lifecycle event
        """
        should_evaluate = False
        reasons = []

        # Check success rate threshold
        if metrics.success_rate < self.success_rate_threshold:
            should_evaluate = True
            reasons.append(
                f"Success rate {metrics.success_rate:.2%} below threshold "
                f"{self.success_rate_threshold:.2%}"
            )

        # Check latency threshold
        if metrics.avg_latency_ms > self.latency_threshold_ms:
            should_evaluate = True
            reasons.append(
                f"Average latency {metrics.avg_latency_ms:.0f}ms above threshold "
                f"{self.latency_threshold_ms:.0f}ms"
            )

        # Check periodic re-evaluation
        if metrics.last_evaluation:
            time_since_eval = datetime.now() - metrics.last_evaluation
            if time_since_eval > self.re_evaluation_interval:
                should_evaluate = True
                reasons.append(
                    f"Periodic re-evaluation due (last: {time_since_eval.total_seconds() / 3600:.1f}h ago)"
                )
        else:
            # First evaluation
            should_evaluate = True
            reasons.append("Initial evaluation")

        # Trigger re-evaluation if needed
        if should_evaluate:
            logger.info(
                f"Triggering re-evaluation for {agent_id}",
                extra={"reasons": reasons}
            )

            await self._trigger_re_evaluation(agent_id, event, reasons)

    async def _trigger_re_evaluation(
        self,
        agent_id: str,
        event: Any,
        reasons: List[str],
    ) -> None:
        """
        Trigger re-evaluation.

        Args:
            agent_id: Agent identifier
            event: Lifecycle event
            reasons: List of trigger reasons
        """
        try:
            # Run evaluation asynchronously
            task = asyncio.create_task(
                self._run_re_evaluation(agent_id, event, reasons)
            )
            logger.info(f"Started re-evaluation task for {agent_id}")
        except Exception as e:
            logger.error(f"Failed to trigger re-evaluation for {agent_id}: {e}")

    async def _run_re_evaluation(
        self,
        agent_id: str,
        event: Any,
        reasons: List[str],
    ) -> None:
        """
        Run re-evaluation task.

        Args:
            agent_id: Agent identifier
            event: Lifecycle event
            reasons: List of trigger reasons
        """
        try:
            result = await self.orchestrator.run(
                agent_spec=event.agent_spec,
                trigger_reason="runtime_monitoring",
                trigger_details={"reasons": reasons}
            )

            # Update last evaluation time
            self._metrics[agent_id].last_evaluation = datetime.now()

            logger.info(
                f"Re-evaluation completed for {agent_id}",
                extra={"status": result.get('status')}
            )
        except Exception as e:
            logger.error(f"Re-evaluation failed for {agent_id}: {e}")

    def get_metrics(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get runtime metrics.

        Args:
            agent_id: Specific agent ID or None for all agents

        Returns:
            Dictionary of metrics
        """
        if agent_id:
            metrics = self._metrics.get(agent_id)
            if metrics:
                return {
                    "agent_id": metrics.agent_id,
                    "total_runs": metrics.total_runs,
                    "successful_runs": metrics.successful_runs,
                    "failed_runs": metrics.failed_runs,
                    "success_rate": metrics.success_rate,
                    "avg_latency_ms": metrics.avg_latency_ms,
                    "last_evaluation": metrics.last_evaluation.isoformat() if metrics.last_evaluation else None,
                }
            return {}

        # Return all metrics
        return {
            aid: {
                "agent_id": m.agent_id,
                "total_runs": m.total_runs,
                "success_rate": m.success_rate,
                "avg_latency_ms": m.avg_latency_ms,
            }
            for aid, m in self._metrics.items()
        }

    def is_running(self) -> bool:
        """Check if monitor is running."""
        return self._running
'''

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        self.files_created.append(file_path)
        logger.info(f"Created: {file_path}")

    async def _create_metrics(self) -> None:
        """Create monitoring module init."""
        file_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "mlte_integration"
            / "monitoring"
            / "__init__.py"
        )

        content = '''"""MLTE Integration Monitoring."""

from mlte_integration.monitoring.runtime_monitor import (
    RuntimeMonitor,
    RuntimeMetrics,
)

__all__ = [
    "RuntimeMonitor",
    "RuntimeMetrics",
]
'''

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        self.files_created.append(file_path)
        logger.info(f"Created: {file_path}")

    async def _create_tests(self) -> None:
        """Create unit tests."""
        test_path = (
            self.workspace_root
            / "python"
            / "tests"
            / "unit"
            / "test_runtime_monitor.py"
        )

        content = '''"""Tests for RuntimeMonitor."""

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
'''

        test_path.parent.mkdir(parents=True, exist_ok=True)
        test_path.write_text(content, encoding='utf-8')
        self.files_created.append(test_path)
        logger.info(f"Created test: {test_path}")

    async def _create_examples(self) -> None:
        """Create usage examples."""
        example_path = (
            self.workspace_root
            / "python"
            / "samples"
            / "mlte_integration"
            / "monitoring_example.py"
        )

        content = '''"""Example: Using RuntimeMonitor."""

from mlte_integration.monitoring import RuntimeMonitor


def main():
    """Demonstrate monitor usage."""
    # Mock orchestrator (replace with real one)
    class MockOrchestrator:
        async def run(self, agent_spec, trigger_reason=None, trigger_details=None):
            print(f"Re-evaluating agent: {agent_spec['name']}")
            print(f"Reason: {trigger_reason}")
            print(f"Details: {trigger_details}")
            return {"status": "completed"}

    orchestrator = MockOrchestrator()

    # Create monitor
    monitor = RuntimeMonitor(
        orchestrator,
        success_rate_threshold=0.90,  # 90% success rate minimum
        latency_threshold_ms=5000.0,  # 5 second maximum
        re_evaluation_interval_hours=24,  # Daily re-evaluation
    )

    # Start monitoring
    monitor.start()
    print("Monitor started - tracking runtime metrics")

    # Monitor will now listen for RUN_COMPLETED and RUN_FAILED events
    # and trigger re-evaluation when thresholds are violated

    # Get metrics
    agent_id = "test-agent"
    metrics = monitor.get_metrics(agent_id)
    if metrics:
        print(f"\\nMetrics for {agent_id}:")
        print(f"  Success rate: {metrics['success_rate']:.2%}")
        print(f"  Avg latency: {metrics['avg_latency_ms']:.0f}ms")

    # Stop when done
    monitor.stop()
    print("\\nMonitor stopped")


if __name__ == "__main__":
    main()
'''

        example_path.parent.mkdir(parents=True, exist_ok=True)
        example_path.write_text(content, encoding='utf-8')
        self.files_created.append(example_path)
        logger.info(f"Created example: {example_path}")


if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO)
    agent = MonitoringImplAgent()
    result = asyncio.run(agent.run())
    print(f"✅ {agent.name} completed: {len(result['files_created'])} files created")
