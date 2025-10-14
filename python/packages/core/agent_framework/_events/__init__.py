"""
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
