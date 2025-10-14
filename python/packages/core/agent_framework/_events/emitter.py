"""
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
