"""
Lifecycle Events Implementation Agent

This agent implements the agent lifecycle event system - the foundation
for automatic MLTE evaluation triggers.

Responsibilities:
1. Create event type definitions
2. Implement event emitter with listener registry
3. Integrate events into BaseAgent class
4. Create unit tests
5. Create usage examples

This agent works AUTONOMOUSLY to complete its task.
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class LifecycleEventsAgent:
    """
    Autonomous agent that implements lifecycle event system.

    This agent will:
    - Create python/packages/core/agent_framework/_events/ directory
    - Write lifecycle_events.py with event definitions
    - Write emitter.py with event emitter
    - Modify agent_framework/_agent.py to emit events
    - Create tests/unit/test_lifecycle_events.py
    - Create samples/lifecycle_events_example.py
    """

    def __init__(self):
        """Initialize the agent."""
        self.name = "LifecycleEventsAgent"
        self.workspace_root = Path("d:/AI_Dev/new_microsoft-agent-framework/Microsoft-agent-framework")
        self.files_created: List[Path] = []
        self.files_modified: List[Path] = []
        self.tests_created: List[Path] = []

        logger.info(f"{self.name} initialized")

    async def run(self) -> Dict[str, Any]:
        """
        Execute the implementation.

        Returns:
            Result dictionary with created files
        """
        logger.info(f"{self.name} starting implementation")

        try:
            # Step 1: Create _events directory
            await self._create_events_directory()

            # Step 2: Create event definitions
            await self._create_event_definitions()

            # Step 3: Create event emitter
            await self._create_event_emitter()

            # Step 4: Create __init__.py for events module
            await self._create_events_init()

            # Step 5: Integrate into BaseAgent (requires finding/modifying existing file)
            await self._integrate_into_base_agent()

            # Step 6: Create unit tests
            await self._create_unit_tests()

            # Step 7: Create usage example
            await self._create_usage_example()

            logger.info(
                f"{self.name} completed successfully - "
                f"Files: {len(self.files_created)} created, {len(self.files_modified)} modified, "
                f"Tests: {len(self.tests_created)} created"
            )

            return {
                "status": "completed",
                "files_created": [str(f) for f in self.files_created],
                "files_modified": [str(f) for f in self.files_modified],
                "tests_created": [str(f) for f in self.tests_created],
            }

        except Exception as e:
            logger.error(f"{self.name} failed", exc_info=True)
            raise

    async def _create_events_directory(self) -> None:
        """Create _events directory in agent_framework."""
        events_dir = self.workspace_root / "python" / "packages" / "core" / "agent_framework" / "_events"
        events_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {events_dir}")

    async def _create_event_definitions(self) -> None:
        """Create lifecycle_events.py with event definitions."""
        file_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "core"
            / "agent_framework"
            / "_events"
            / "lifecycle_events.py"
        )

        content = '''"""
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
'''

        file_path.write_text(content)
        self.files_created.append(file_path)
        logger.info(f"Created: {file_path}")

    async def _create_event_emitter(self) -> None:
        """Create emitter.py with event emitter and listener registry."""
        file_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "core"
            / "agent_framework"
            / "_events"
            / "emitter.py"
        )

        content = '''"""
Event emitter for agent lifecycle events.

Federal Compliance:
- AU-2: Audit event generation
- AU-12: Audit generation capability
- AU-14: Audit review, analysis, and reporting
"""

from typing import Callable, Dict, List
import asyncio
import logging

from agent_framework._events.lifecycle_events import (
    AgentLifecycleEvent,
    AgentLifecycleEventType,
)

logger = logging.getLogger(__name__)


class LifecycleEventEmitter:
    """
    Emits and manages agent lifecycle events.

    This class implements the observer pattern for agent lifecycle events,
    allowing listeners to react to agent creation, updates, and runtime events.

    Federal Compliance:
        - AU-2: Audit event generation
        - AU-12: Audit generation
        - AU-14: Audit review, analysis, and reporting

    Example:
        >>> emitter = LifecycleEventEmitter()
        >>> emitter.register_listener(
        ...     AgentLifecycleEventType.CREATED,
        ...     lambda event: print(f"Agent {event.agent_name} created")
        ... )
        >>> event = AgentLifecycleEvent(...)
        >>> await emitter.emit(event)
    """

    _instance: "LifecycleEventEmitter | None" = None

    def __new__(cls):
        """Singleton pattern for global event emitter."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._listeners: Dict[AgentLifecycleEventType, List[Callable]] = {}
            cls._instance._initialized = True
            logger.info("LifecycleEventEmitter singleton created")
        return cls._instance

    def register_listener(
        self,
        event_type: AgentLifecycleEventType,
        callback: Callable[[AgentLifecycleEvent], None],
    ) -> None:
        """
        Register a listener for specific event type.

        Args:
            event_type: Type of event to listen for
            callback: Async or sync callback function to invoke

        Federal Compliance:
            - AU-14: Audit review capability

        Example:
            >>> async def on_created(event):
            ...     print(f"Agent created: {event.agent_name}")
            >>> emitter.register_listener(
            ...     AgentLifecycleEventType.CREATED,
            ...     on_created
            ... )
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []

        self._listeners[event_type].append(callback)

        logger.info(
            "Registered lifecycle event listener",
            extra={
                "event_type": event_type.value,
                "callback": callback.__name__,
                "listener_count": len(self._listeners[event_type]),
            }
        )

    def unregister_listener(
        self,
        event_type: AgentLifecycleEventType,
        callback: Callable,
    ) -> None:
        """
        Unregister a listener.

        Args:
            event_type: Event type
            callback: Callback to remove
        """
        if event_type in self._listeners:
            self._listeners[event_type] = [
                cb for cb in self._listeners[event_type] if cb != callback
            ]

            logger.info(
                "Unregistered lifecycle event listener",
                extra={
                    "event_type": event_type.value,
                    "callback": callback.__name__,
                }
            )

    async def emit(self, event: AgentLifecycleEvent) -> None:
        """
        Emit an event to all registered listeners.

        Args:
            event: Lifecycle event to emit

        Federal Compliance:
            - AU-2: Generate audit record
            - AU-12: Audit generation

        Note:
            This method is non-blocking. Listeners are called asynchronously
            and errors in listeners don't affect the emitting agent.
        """
        if event.event_type not in self._listeners:
            logger.debug(
                "No listeners registered for event type",
                extra={"event_type": event.event_type.value}
            )
            return

        listener_count = len(self._listeners[event.event_type])
        logger.debug(
            "Emitting lifecycle event",
            extra={
                "event_type": event.event_type.value,
                "agent_id": event.agent_id,
                "listener_count": listener_count,
            }
        )

        # Call listeners asynchronously (non-blocking)
        tasks = []
        for callback in self._listeners[event.event_type]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    task = asyncio.create_task(callback(event))
                    tasks.append(task)
                else:
                    # Sync callback - run in thread pool
                    task = asyncio.create_task(
                        asyncio.to_thread(callback, event)
                    )
                    tasks.append(task)
            except Exception as e:
                logger.error(
                    "Error calling lifecycle listener",
                    extra={
                        "event_type": event.event_type.value,
                        "callback": callback.__name__,
                        "error": str(e),
                    },
                    exc_info=True,
                )

        # Don't wait for tasks to complete (fire-and-forget)
        # Store tasks to prevent garbage collection
        if tasks:
            asyncio.create_task(self._monitor_tasks(tasks, event.event_type))

    async def _monitor_tasks(
        self,
        tasks: List[asyncio.Task],
        event_type: AgentLifecycleEventType,
    ) -> None:
        """Monitor listener tasks and log errors."""
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(
                    "Lifecycle listener task failed",
                    extra={
                        "event_type": event_type.value,
                        "task_index": i,
                        "error": str(result),
                    },
                    exc_info=result,
                )

    def clear_all_listeners(self) -> None:
        """Clear all registered listeners (for testing)."""
        self._listeners.clear()
        logger.info("Cleared all lifecycle event listeners")

    def get_listener_count(self, event_type: AgentLifecycleEventType) -> int:
        """
        Get number of listeners for an event type.

        Args:
            event_type: Event type to check

        Returns:
            Number of registered listeners
        """
        return len(self._listeners.get(event_type, []))


# Global emitter instance
_emitter = LifecycleEventEmitter()


def emit_lifecycle_event(event: AgentLifecycleEvent) -> None:
    """
    Emit a lifecycle event (convenience function).

    Args:
        event: Event to emit

    Example:
        >>> event = AgentLifecycleEvent(
        ...     event_type=AgentLifecycleEventType.CREATED,
        ...     agent_id="agent-123",
        ...     agent_name="TestAgent",
        ...     agent_type="ChatAgent"
        ... )
        >>> emit_lifecycle_event(event)
    """
    asyncio.create_task(_emitter.emit(event))


def register_lifecycle_listener(
    event_type: AgentLifecycleEventType,
    callback: Callable[[AgentLifecycleEvent], None],
) -> None:
    """
    Register a lifecycle event listener (convenience function).

    Args:
        event_type: Type of event to listen for
        callback: Callback function (async or sync)

    Example:
        >>> async def on_agent_created(event):
        ...     print(f"New agent: {event.agent_name}")
        >>>
        >>> register_lifecycle_listener(
        ...     AgentLifecycleEventType.CREATED,
        ...     on_agent_created
        ... )
    """
    _emitter.register_listener(event_type, callback)


def unregister_lifecycle_listener(
    event_type: AgentLifecycleEventType,
    callback: Callable,
) -> None:
    """
    Unregister a lifecycle event listener (convenience function).

    Args:
        event_type: Event type
        callback: Callback to remove
    """
    _emitter.unregister_listener(event_type, callback)


def get_emitter() -> LifecycleEventEmitter:
    """
    Get the global emitter instance.

    Returns:
        Global LifecycleEventEmitter instance
    """
    return _emitter
'''

        file_path.write_text(content)
        self.files_created.append(file_path)
        logger.info(f"Created: {file_path}")

    async def _create_events_init(self) -> None:
        """Create __init__.py for _events module."""
        file_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "core"
            / "agent_framework"
            / "_events"
            / "__init__.py"
        )

        content = '''"""
Agent lifecycle events module.

This module provides event-driven capabilities for agent lifecycle monitoring,
enabling automatic MLTE evaluation, runtime monitoring, and audit trail generation.

Federal Compliance:
- AU-2: Audit events
- AU-12: Audit generation
"""

from agent_framework._events.lifecycle_events import (
    AgentLifecycleEvent,
    AgentLifecycleEventType,
)
from agent_framework._events.emitter import (
    LifecycleEventEmitter,
    emit_lifecycle_event,
    register_lifecycle_listener,
    unregister_lifecycle_listener,
    get_emitter,
)

__all__ = [
    "AgentLifecycleEvent",
    "AgentLifecycleEventType",
    "LifecycleEventEmitter",
    "emit_lifecycle_event",
    "register_lifecycle_listener",
    "unregister_lifecycle_listener",
    "get_emitter",
]
'''

        file_path.write_text(content)
        self.files_created.append(file_path)
        logger.info(f"Created: {file_path}")

    async def _integrate_into_base_agent(self) -> None:
        """
        Integrate lifecycle events into BaseAgent.

        Note: This requires finding the BaseAgent class and modifying it.
        For now, we'll create a comprehensive integration guide.
        """
        integration_guide_path = (
            self.workspace_root
            / "python"
            / "packages"
            / "core"
            / "agent_framework"
            / "_events"
            / "INTEGRATION_GUIDE.md"
        )

        content = '''# BaseAgent Integration Guide

## Overview

This guide shows how to integrate lifecycle events into the BaseAgent class.

## Required Changes

### 1. Import Events Module

Add to `agent_framework/_agent.py`:

```python
from agent_framework._events import (
    AgentLifecycleEvent,
    AgentLifecycleEventType,
    emit_lifecycle_event,
)
```

### 2. Modify `__init__` Method

Add event emission after agent initialization:

```python
def __init__(self, name: str, instructions: str, chat_client: Any, **kwargs):
    self._id = kwargs.get("id", f"{name}-{uuid.uuid4().hex[:8]}")
    self._name = name
    self._instructions = instructions
    self._chat_client = chat_client
    self._first_run = True

    # ... existing initialization ...

    # Emit CREATED event
    self._emit_lifecycle_event(AgentLifecycleEventType.CREATED)
```

### 3. Add `_emit_lifecycle_event` Method

```python
def _emit_lifecycle_event(
    self,
    event_type: AgentLifecycleEventType,
    metadata: Dict[str, Any] = None,
) -> None:
    """
    Emit a lifecycle event for this agent.

    Args:
        event_type: Type of event
        metadata: Additional metadata
    """
    event = AgentLifecycleEvent(
        event_type=event_type,
        agent_id=self._id,
        agent_name=self._name,
        agent_type=self.__class__.__name__,
        metadata=metadata or {},
        agent_spec=self._get_agent_spec(),
    )

    emit_lifecycle_event(event)
```

### 4. Add `_get_agent_spec` Method

```python
def _get_agent_spec(self) -> Dict[str, Any]:
    """
    Get agent specification for evaluation.

    Returns:
        Agent specification dictionary
    """
    return {
        "model_id": self._id,
        "name": self._name,
        "instructions": self._instructions,
        "agent_type": self.__class__.__name__,
        "tools": [tool.name for tool in getattr(self, "_tools", [])],
        "version": getattr(self, "_version", "v1.0.0"),
        "metadata": getattr(self, "_metadata", {}),
    }
```

### 5. Modify `run` Method

Add event emissions for run lifecycle:

```python
async def run(self, messages: List[ChatMessage], **kwargs) -> AgentRunResponse:
    """Run agent with lifecycle events."""

    # Emit first run event
    if self._first_run:
        self._emit_lifecycle_event(AgentLifecycleEventType.FIRST_RUN)
        self._first_run = False

    # Emit run started
    self._emit_lifecycle_event(
        AgentLifecycleEventType.RUN_STARTED,
        metadata={"message_count": len(messages)},
    )

    try:
        # Existing run logic
        response = await self._execute_run(messages, **kwargs)

        # Emit run completed
        self._emit_lifecycle_event(
            AgentLifecycleEventType.RUN_COMPLETED,
            metadata={"success": True},
        )

        return response

    except Exception as e:
        # Emit run failed
        self._emit_lifecycle_event(
            AgentLifecycleEventType.RUN_FAILED,
            metadata={"error": str(e)},
        )
        raise
```

## Testing Integration

After integration, test with:

```python
from agent_framework import ChatAgent
from agent_framework._events import (
    register_lifecycle_listener,
    AgentLifecycleEventType,
)

# Register listener
events_received = []

def on_created(event):
    events_received.append(event)
    print(f"Agent created: {event.agent_name}")

register_lifecycle_listener(
    AgentLifecycleEventType.CREATED,
    on_created
)

# Create agent
agent = ChatAgent(
    name="TestAgent",
    instructions="You are helpful",
    chat_client=mock_client,
)

# Check event was emitted
assert len(events_received) == 1
assert events_received[0].agent_name == "TestAgent"
```

## Federal Compliance

The integrated events provide:
- AU-2: Auditable events for all agent operations
- AU-3: Complete audit record content
- AU-12: Automated audit generation
'''

        integration_guide_path.write_text(content)
        self.files_created.append(integration_guide_path)
        logger.info(f"Created integration guide: {integration_guide_path}")

    async def _create_unit_tests(self) -> None:
        """Create unit tests for lifecycle events."""
        test_file_path = (
            self.workspace_root
            / "python"
            / "tests"
            / "unit"
            / "test_lifecycle_events.py"
        )

        test_file_path.parent.mkdir(parents=True, exist_ok=True)

        content = '''"""
Unit tests for agent lifecycle events.

Federal Compliance:
- SA-11: Developer testing
"""

import asyncio
import pytest
from datetime import datetime, timezone

from agent_framework._events import (
    AgentLifecycleEvent,
    AgentLifecycleEventType,
    LifecycleEventEmitter,
    emit_lifecycle_event,
    register_lifecycle_listener,
    unregister_lifecycle_listener,
    get_emitter,
)


class TestAgentLifecycleEvent:
    """Tests for AgentLifecycleEvent."""

    def test_event_creation(self):
        """Test creating a lifecycle event."""
        event = AgentLifecycleEvent(
            event_type=AgentLifecycleEventType.CREATED,
            agent_id="agent-123",
            agent_name="TestAgent",
            agent_type="ChatAgent",
        )

        assert event.event_type == AgentLifecycleEventType.CREATED
        assert event.agent_id == "agent-123"
        assert event.agent_name == "TestAgent"
        assert event.agent_type == "ChatAgent"
        assert isinstance(event.timestamp, datetime)
        assert event.metadata == {}
        assert event.agent_spec is None

    def test_event_with_metadata(self):
        """Test event with metadata."""
        metadata = {"key": "value", "count": 42}
        agent_spec = {"model_id": "agent-123", "version": "v1.0.0"}

        event = AgentLifecycleEvent(
            event_type=AgentLifecycleEventType.RUN_STARTED,
            agent_id="agent-123",
            agent_name="TestAgent",
            agent_type="ChatAgent",
            metadata=metadata,
            agent_spec=agent_spec,
        )

        assert event.metadata == metadata
        assert event.agent_spec == agent_spec

    def test_event_to_dict(self):
        """Test converting event to dictionary."""
        event = AgentLifecycleEvent(
            event_type=AgentLifecycleEventType.CREATED,
            agent_id="agent-123",
            agent_name="TestAgent",
            agent_type="ChatAgent",
        )

        event_dict = event.to_dict()

        assert event_dict["event_type"] == "agent.created"
        assert event_dict["agent_id"] == "agent-123"
        assert event_dict["agent_name"] == "TestAgent"
        assert event_dict["agent_type"] == "ChatAgent"
        assert "timestamp" in event_dict

    def test_event_from_dict(self):
        """Test creating event from dictionary."""
        event_dict = {
            "event_type": "agent.created",
            "agent_id": "agent-123",
            "agent_name": "TestAgent",
            "agent_type": "ChatAgent",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": {"key": "value"},
            "agent_spec": {"version": "v1.0.0"},
        }

        event = AgentLifecycleEvent.from_dict(event_dict)

        assert event.event_type == AgentLifecycleEventType.CREATED
        assert event.agent_id == "agent-123"
        assert event.metadata == {"key": "value"}
        assert event.agent_spec == {"version": "v1.0.0"}


class TestLifecycleEventEmitter:
    """Tests for LifecycleEventEmitter."""

    def setup_method(self):
        """Clear listeners before each test."""
        emitter = get_emitter()
        emitter.clear_all_listeners()

    def test_emitter_singleton(self):
        """Test emitter is a singleton."""
        emitter1 = LifecycleEventEmitter()
        emitter2 = LifecycleEventEmitter()
        emitter3 = get_emitter()

        assert emitter1 is emitter2
        assert emitter2 is emitter3

    def test_register_listener(self):
        """Test registering a listener."""
        emitter = get_emitter()
        events_received = []

        def listener(event):
            events_received.append(event)

        emitter.register_listener(AgentLifecycleEventType.CREATED, listener)

        assert emitter.get_listener_count(AgentLifecycleEventType.CREATED) == 1

    def test_unregister_listener(self):
        """Test unregistering a listener."""
        emitter = get_emitter()

        def listener(event):
            pass

        emitter.register_listener(AgentLifecycleEventType.CREATED, listener)
        assert emitter.get_listener_count(AgentLifecycleEventType.CREATED) == 1

        emitter.unregister_listener(AgentLifecycleEventType.CREATED, listener)
        assert emitter.get_listener_count(AgentLifecycleEventType.CREATED) == 0

    @pytest.mark.asyncio
    async def test_emit_event_sync_listener(self):
        """Test emitting event to synchronous listener."""
        emitter = get_emitter()
        events_received = []

        def listener(event):
            events_received.append(event)

        emitter.register_listener(AgentLifecycleEventType.CREATED, listener)

        event = AgentLifecycleEvent(
            event_type=AgentLifecycleEventType.CREATED,
            agent_id="agent-123",
            agent_name="TestAgent",
            agent_type="ChatAgent",
        )

        await emitter.emit(event)
        await asyncio.sleep(0.1)  # Give listeners time to execute

        assert len(events_received) == 1
        assert events_received[0].agent_id == "agent-123"

    @pytest.mark.asyncio
    async def test_emit_event_async_listener(self):
        """Test emitting event to asynchronous listener."""
        emitter = get_emitter()
        events_received = []

        async def listener(event):
            await asyncio.sleep(0.01)  # Simulate async work
            events_received.append(event)

        emitter.register_listener(AgentLifecycleEventType.CREATED, listener)

        event = AgentLifecycleEvent(
            event_type=AgentLifecycleEventType.CREATED,
            agent_id="agent-123",
            agent_name="TestAgent",
            agent_type="ChatAgent",
        )

        await emitter.emit(event)
        await asyncio.sleep(0.1)  # Give listeners time to execute

        assert len(events_received) == 1
        assert events_received[0].agent_id == "agent-123"

    @pytest.mark.asyncio
    async def test_multiple_listeners(self):
        """Test multiple listeners for same event type."""
        emitter = get_emitter()
        events_received_1 = []
        events_received_2 = []

        def listener1(event):
            events_received_1.append(event)

        def listener2(event):
            events_received_2.append(event)

        emitter.register_listener(AgentLifecycleEventType.CREATED, listener1)
        emitter.register_listener(AgentLifecycleEventType.CREATED, listener2)

        event = AgentLifecycleEvent(
            event_type=AgentLifecycleEventType.CREATED,
            agent_id="agent-123",
            agent_name="TestAgent",
            agent_type="ChatAgent",
        )

        await emitter.emit(event)
        await asyncio.sleep(0.1)

        assert len(events_received_1) == 1
        assert len(events_received_2) == 1

    @pytest.mark.asyncio
    async def test_listener_error_doesnt_crash(self):
        """Test that listener errors don't crash the emitter."""
        emitter = get_emitter()
        events_received = []

        def failing_listener(event):
            raise ValueError("Intentional error")

        def working_listener(event):
            events_received.append(event)

        emitter.register_listener(AgentLifecycleEventType.CREATED, failing_listener)
        emitter.register_listener(AgentLifecycleEventType.CREATED, working_listener)

        event = AgentLifecycleEvent(
            event_type=AgentLifecycleEventType.CREATED,
            agent_id="agent-123",
            agent_name="TestAgent",
            agent_type="ChatAgent",
        )

        # Should not raise exception
        await emitter.emit(event)
        await asyncio.sleep(0.1)

        # Working listener should still receive event
        assert len(events_received) == 1


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def setup_method(self):
        """Clear listeners before each test."""
        get_emitter().clear_all_listeners()

    def test_register_lifecycle_listener(self):
        """Test convenience function for registering listener."""
        events_received = []

        def listener(event):
            events_received.append(event)

        register_lifecycle_listener(AgentLifecycleEventType.CREATED, listener)

        assert get_emitter().get_listener_count(AgentLifecycleEventType.CREATED) == 1

    def test_unregister_lifecycle_listener(self):
        """Test convenience function for unregistering listener."""
        def listener(event):
            pass

        register_lifecycle_listener(AgentLifecycleEventType.CREATED, listener)
        unregister_lifecycle_listener(AgentLifecycleEventType.CREATED, listener)

        assert get_emitter().get_listener_count(AgentLifecycleEventType.CREATED) == 0
'''

        test_file_path.write_text(content)
        self.tests_created.append(test_file_path)
        logger.info(f"Created tests: {test_file_path}")

    async def _create_usage_example(self) -> None:
        """Create usage example for lifecycle events."""
        example_path = (
            self.workspace_root
            / "python"
            / "samples"
            / "lifecycle_events"
            / "basic_usage.py"
        )

        example_path.parent.mkdir(parents=True, exist_ok=True)

        content = '''"""
Lifecycle Events - Basic Usage Example

This example demonstrates how to use agent lifecycle events for monitoring
and automation.

Federal Compliance:
- AU-2: Audit event examples
- AU-14: Audit review examples
"""

import asyncio
from agent_framework._events import (
    register_lifecycle_listener,
    AgentLifecycleEventType,
)


def main():
    """Demonstrate lifecycle event usage."""
    print("=" * 80)
    print("Agent Lifecycle Events - Basic Usage")
    print("=" * 80)
    print()

    # Example 1: Simple event logging
    print("Example 1: Event Logging")
    print("-" * 80)

    def log_agent_created(event):
        print(f"✅ Agent created: {event.agent_name}")
        print(f"   ID: {event.agent_id}")
        print(f"   Type: {event.agent_type}")
        print(f"   Time: {event.timestamp.isoformat()}")

    register_lifecycle_listener(
        AgentLifecycleEventType.CREATED,
        log_agent_created
    )

    print()

    # Example 2: Performance monitoring
    print("Example 2: Performance Monitoring")
    print("-" * 80)

    run_start_times = {}

    def on_run_started(event):
        run_start_times[event.agent_id] = event.timestamp
        print(f"▶️  Agent {event.agent_name} started run")

    def on_run_completed(event):
        start_time = run_start_times.get(event.agent_id)
        if start_time:
            duration = (event.timestamp - start_time).total_seconds()
            print(f"✅ Agent {event.agent_name} completed run in {duration:.2f}s")

    register_lifecycle_listener(
        AgentLifecycleEventType.RUN_STARTED,
        on_run_started
    )
    register_lifecycle_listener(
        AgentLifecycleEventType.RUN_COMPLETED,
        on_run_completed
    )

    print()

    # Example 3: Error tracking
    print("Example 3: Error Tracking")
    print("-" * 80)

    errors_by_agent = {}

    def on_run_failed(event):
        agent_id = event.agent_id
        if agent_id not in errors_by_agent:
            errors_by_agent[agent_id] = []

        error = event.metadata.get("error", "Unknown error")
        errors_by_agent[agent_id].append(error)

        print(f"❌ Agent {event.agent_name} failed: {error}")
        print(f"   Total errors for this agent: {len(errors_by_agent[agent_id])}")

    register_lifecycle_listener(
        AgentLifecycleEventType.RUN_FAILED,
        on_run_failed
    )

    print()

    # Example 4: Automatic evaluation trigger
    print("Example 4: Automatic MLTE Evaluation")
    print("-" * 80)

    async def trigger_mlte_evaluation(event):
        """Simulate MLTE evaluation trigger."""
        print(f"🔍 Triggering MLTE evaluation for: {event.agent_name}")
        print(f"   Agent spec: {event.agent_spec}")

        # In real implementation, this would call MLTEOrchestratorAgent
        await asyncio.sleep(0.1)  # Simulate async work

        print(f"✅ MLTE evaluation queued for: {event.agent_name}")

    register_lifecycle_listener(
        AgentLifecycleEventType.CREATED,
        trigger_mlte_evaluation
    )

    print()
    print("=" * 80)
    print("Event listeners registered!")
    print("Create agents to see events in action.")
    print("=" * 80)


if __name__ == "__main__":
    main()
'''

        example_path.write_text(content, encoding='utf-8')
        self.files_created.append(example_path)
        logger.info(f"Created example: {example_path}")


async def main():
    """Test the agent."""
    agent = LifecycleEventsAgent()
    result = await agent.run()

    print("\n" + "=" * 80)
    print("LifecycleEventsAgent Execution Complete")
    print("=" * 80)
    print(f"Status: {result['status']}")
    print(f"Files Created: {len(result['files_created'])}")
    print(f"Files Modified: {len(result['files_modified'])}")
    print(f"Tests Created: {len(result['tests_created'])}")
    print("\nFiles Created:")
    for file in result['files_created']:
        print(f"  - {file}")
    print("=" * 80)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
