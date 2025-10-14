"""
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
