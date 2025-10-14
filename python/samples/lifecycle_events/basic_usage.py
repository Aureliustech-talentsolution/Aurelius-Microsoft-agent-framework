"""
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
