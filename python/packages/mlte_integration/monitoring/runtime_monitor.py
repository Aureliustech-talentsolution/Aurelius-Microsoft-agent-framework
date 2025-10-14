"""
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
