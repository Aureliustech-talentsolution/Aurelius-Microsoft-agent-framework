# BaseAgent Integration Guide

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
