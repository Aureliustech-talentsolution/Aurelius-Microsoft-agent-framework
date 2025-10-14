"""
Agent lifecycle events for MLTE integration and monitoring.

Federal Compliance:
- AU-2: Audit events
- AU-12: Audit generation
- AU-3: Content of audit records
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AgentLifecycleEventType(str, Enum):
    """Types of agent lifecycle events."""
    
    CREATED = "agent.created"
    INITIALIZED = "agent.initialized"
    FIRST_RUN = "agent.first_run"
    RUN_STARTED = "agent.run_started"
    RUN_COMPLETED = "agent.run_completed"
    RUN_FAILED = "agent.run_failed"
    UPDATED = "agent.updated"
    DECOMMISSIONED = "agent.decommissioned"


@dataclass
class AgentLifecycleEvent:
    """
    Event emitted during agent lifecycle.
    
    Attributes:
        event_type: Type of lifecycle event
        agent_id: Unique identifier for the agent
        agent_name: Human-readable agent name
        agent_type: Type of agent (ChatAgent, WorkflowAgent, etc.)
        timestamp: Event timestamp (UTC)
        metadata: Additional event metadata
        agent_spec: Agent specification (for evaluation)
    
    Federal Compliance:
        - AU-2: Auditable event
        - AU-3: Content of audit records
        - AU-12: Audit generation
    
    Example:
        >>> event = AgentLifecycleEvent(
        ...     event_type=AgentLifecycleEventType.CREATED,
        ...     agent_id="agent-123",
        ...     agent_name="CustomerServiceAgent",
        ...     agent_type="ChatAgent"
        ... )
    """
    
    event_type: AgentLifecycleEventType
    agent_id: str
    agent_name: str
    agent_type: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)
    agent_spec: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Log event creation for audit trail."""
        logger.info(
            "Agent lifecycle event created",
            extra={
                "event_type": self.event_type.value,
                "agent_id": self.agent_id,
                "agent_name": self.agent_name,
                "agent_type": self.agent_type,
                "timestamp": self.timestamp.isoformat(),
            }
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary for serialization.
        
        Returns:
            Dictionary representation of event
        
        Federal Compliance:
            - AU-3: Audit record content
        """
        return {
            "event_type": self.event_type.value,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "agent_spec": self.agent_spec,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentLifecycleEvent":
        """
        Create event from dictionary.
        
        Args:
            data: Dictionary representation
        
        Returns:
            AgentLifecycleEvent instance
        """
        return cls(
            event_type=AgentLifecycleEventType(data["event_type"]),
            agent_id=data["agent_id"],
            agent_name=data["agent_name"],
            agent_type=data["agent_type"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
            agent_spec=data.get("agent_spec"),
        )
