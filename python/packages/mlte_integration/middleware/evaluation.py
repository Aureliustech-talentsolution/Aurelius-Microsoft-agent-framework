"""
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
