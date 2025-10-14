"""
MiddlewareImplAgent - Full Implementation

Implements MLTEEvaluationMiddleware that automatically triggers
MLTE evaluation when agents are created or updated.

Event-driven architecture with configurable execution modes.
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class MiddlewareImplAgent:
    """Autonomous agent that implements MLTEEvaluationMiddleware."""

    def __init__(self):
        self.name = "MiddlewareImplAgent"
        self.workspace_root = Path("d:/AI_Dev/new_microsoft-agent-framework/Microsoft-agent-framework")
        self.files_created: List[Path] = []
        logger.info(f"{self.name} initialized")

    async def run(self) -> Dict[str, Any]:
        """Execute the implementation."""
        logger.info(f"{self.name} starting full implementation")

        try:
            # Create middleware file
            await self._create_middleware()

            # Create configuration file
            await self._create_config()

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

    async def _create_middleware(self) -> None:
        """Create MLTEEvaluationMiddleware."""
        file_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "mlte_integration"
            / "middleware"
            / "evaluation.py"
        )

        content = '''"""
MLTEEvaluationMiddleware - Automatic MLTE Evaluation Trigger

Listens for lifecycle events and automatically triggers MLTE evaluation.

Federal Compliance: SA-11 (Developer Testing), CA-8 (Continuous Monitoring)
"""

from typing import Dict, Any, Set, Optional
import logging
import asyncio
from enum import Enum

logger = logging.getLogger(__name__)


class EvaluationMode(Enum):
    """Evaluation execution modes."""
    SYNCHRONOUS = "synchronous"  # Block until evaluation completes
    ASYNCHRONOUS = "asynchronous"  # Run evaluation in background
    CI_ONLY = "ci_only"  # Only run in CI/CD pipelines


class MLTEEvaluationMiddleware:
    """
    Automatically triggers MLTE evaluation on agent lifecycle events.

    Listens for:
    - CREATED: Agent first created
    - FIRST_RUN: Agent first execution
    - UPDATED: Agent modified

    Supports multiple execution modes:
    - Synchronous: Block until evaluation completes
    - Asynchronous: Run evaluation in background
    - CI-only: Only run in CI/CD environment

    Federal Compliance: SA-11, CA-8
    """

    def __init__(
        self,
        orchestrator: Any,  # MLTEOrchestratorAgent
        mode: EvaluationMode = EvaluationMode.ASYNCHRONOUS,
        trigger_on_create: bool = True,
        trigger_on_first_run: bool = True,
        trigger_on_update: bool = True,
    ):
        """
        Initialize middleware.

        Args:
            orchestrator: MLTEOrchestratorAgent instance
            mode: Execution mode
            trigger_on_create: Trigger on CREATED event
            trigger_on_first_run: Trigger on FIRST_RUN event
            trigger_on_update: Trigger on UPDATED event
        """
        self.orchestrator = orchestrator
        self.mode = mode
        self.trigger_on_create = trigger_on_create
        self.trigger_on_first_run = trigger_on_first_run
        self.trigger_on_update = trigger_on_update

        # De-duplication tracking
        self._evaluated_agents: Set[str] = set()
        self._running = False

        logger.info(
            f"MLTEEvaluationMiddleware initialized",
            extra={
                "mode": mode.value,
                "trigger_on_create": trigger_on_create,
                "trigger_on_first_run": trigger_on_first_run,
                "trigger_on_update": trigger_on_update,
            }
        )

    def start(self) -> None:
        """
        Start listening for lifecycle events.

        Registers event listeners based on configuration.
        """
        if self._running:
            logger.warning("Middleware already running")
            return

        from agent_framework._events import (
            register_lifecycle_listener,
            AgentLifecycleEventType,
        )

        if self.trigger_on_create:
            register_lifecycle_listener(
                AgentLifecycleEventType.CREATED,
                self._on_agent_created
            )
            logger.info("Registered listener for CREATED events")

        if self.trigger_on_first_run:
            register_lifecycle_listener(
                AgentLifecycleEventType.FIRST_RUN,
                self._on_first_run
            )
            logger.info("Registered listener for FIRST_RUN events")

        if self.trigger_on_update:
            register_lifecycle_listener(
                AgentLifecycleEventType.UPDATED,
                self._on_agent_updated
            )
            logger.info("Registered listener for UPDATED events")

        self._running = True
        logger.info("MLTEEvaluationMiddleware started")

    def stop(self) -> None:
        """Stop listening for events."""
        # TODO: Implement unregistering listeners
        self._running = False
        logger.info("MLTEEvaluationMiddleware stopped")

    async def _on_agent_created(self, event: Any) -> None:
        """
        Handle CREATED event.

        Args:
            event: AgentLifecycleEvent
        """
        logger.info(
            f"Agent CREATED: {event.agent_id}",
            extra={"agent_name": event.agent_spec.get('name')}
        )

        await self._trigger_evaluation(event)

    async def _on_first_run(self, event: Any) -> None:
        """
        Handle FIRST_RUN event.

        Args:
            event: AgentLifecycleEvent
        """
        logger.info(f"Agent FIRST_RUN: {event.agent_id}")
        await self._trigger_evaluation(event)

    async def _on_agent_updated(self, event: Any) -> None:
        """
        Handle UPDATED event.

        Args:
            event: AgentLifecycleEvent
        """
        logger.info(
            f"Agent UPDATED: {event.agent_id}",
            extra={"changes": event.metadata.get('changes', [])}
        )

        # Remove from evaluated set to allow re-evaluation
        self._evaluated_agents.discard(event.agent_id)

        await self._trigger_evaluation(event)

    async def _trigger_evaluation(self, event: Any) -> None:
        """
        Trigger MLTE evaluation.

        Args:
            event: AgentLifecycleEvent
        """
        # Check de-duplication
        if event.agent_id in self._evaluated_agents:
            logger.info(f"Skipping duplicate evaluation for {event.agent_id}")
            return

        # Check CI-only mode
        if self.mode == EvaluationMode.CI_ONLY:
            import os
            if not os.environ.get('CI'):
                logger.info("Skipping evaluation (CI_ONLY mode, not in CI)")
                return

        # Mark as evaluated
        self._evaluated_agents.add(event.agent_id)

        logger.info(
            f"Triggering evaluation for {event.agent_id}",
            extra={"mode": self.mode.value}
        )

        # Execute based on mode
        if self.mode == EvaluationMode.SYNCHRONOUS:
            await self._run_synchronous(event)
        else:  # ASYNCHRONOUS or CI_ONLY
            await self._run_asynchronous(event)

    async def _run_synchronous(self, event: Any) -> None:
        """Run evaluation synchronously."""
        try:
            result = await self.orchestrator.run(agent_spec=event.agent_spec)
            logger.info(
                f"Evaluation completed for {event.agent_id}",
                extra={"status": result.get('status')}
            )
        except Exception as e:
            logger.error(f"Evaluation failed for {event.agent_id}: {e}")

    async def _run_asynchronous(self, event: Any) -> None:
        """Run evaluation asynchronously."""
        task = asyncio.create_task(
            self._run_evaluation_task(event)
        )
        logger.info(f"Started background evaluation for {event.agent_id}")

    async def _run_evaluation_task(self, event: Any) -> None:
        """Background evaluation task."""
        try:
            result = await self.orchestrator.run(agent_spec=event.agent_spec)
            logger.info(
                f"Background evaluation completed for {event.agent_id}",
                extra={"status": result.get('status')}
            )
        except Exception as e:
            logger.error(f"Background evaluation failed for {event.agent_id}: {e}")

    def get_evaluated_agents(self) -> Set[str]:
        """Get set of evaluated agent IDs."""
        return self._evaluated_agents.copy()

    def is_running(self) -> bool:
        """Check if middleware is running."""
        return self._running
'''

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        self.files_created.append(file_path)
        logger.info(f"Created: {file_path}")

    async def _create_config(self) -> None:
        """Create configuration utilities."""
        file_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "mlte_integration"
            / "middleware"
            / "__init__.py"
        )

        content = '''"""MLTE Integration Middleware."""

from mlte_integration.middleware.evaluation import (
    MLTEEvaluationMiddleware,
    EvaluationMode,
)

__all__ = [
    "MLTEEvaluationMiddleware",
    "EvaluationMode",
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
            / "test_middleware.py"
        )

        content = '''"""Tests for MLTEEvaluationMiddleware."""

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
            / "middleware_example.py"
        )

        content = '''"""Example: Using MLTEEvaluationMiddleware."""

from mlte_integration.middleware import MLTEEvaluationMiddleware, EvaluationMode


def main():
    """Demonstrate middleware usage."""
    # Mock orchestrator (replace with real one)
    class MockOrchestrator:
        async def run(self, agent_spec):
            print(f"Evaluating agent: {agent_spec['name']}")
            return {"status": "completed"}

    orchestrator = MockOrchestrator()

    # Create middleware
    middleware = MLTEEvaluationMiddleware(
        orchestrator,
        mode=EvaluationMode.ASYNCHRONOUS,
        trigger_on_create=True,
        trigger_on_first_run=True,
        trigger_on_update=True,
    )

    # Start listening
    middleware.start()
    print("Middleware started - listening for events")

    # Now when agents are created/updated, evaluation will trigger automatically
    # Example: agent_framework will emit CREATED event -> middleware triggers evaluation

    # Check status
    print(f"Running: {middleware.is_running()}")
    print(f"Evaluated agents: {len(middleware.get_evaluated_agents())}")

    # Stop when done
    middleware.stop()
    print("Middleware stopped")


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
    agent = MiddlewareImplAgent()
    result = asyncio.run(agent.run())
    print(f"✅ {agent.name} completed: {len(result['files_created'])} files created")
