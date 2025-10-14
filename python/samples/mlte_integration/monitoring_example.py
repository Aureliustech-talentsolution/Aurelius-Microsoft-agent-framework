"""Example: Using RuntimeMonitor."""

from mlte_integration.monitoring import RuntimeMonitor


def main():
    """Demonstrate monitor usage."""
    # Mock orchestrator (replace with real one)
    class MockOrchestrator:
        async def run(self, agent_spec, trigger_reason=None, trigger_details=None):
            print(f"Re-evaluating agent: {agent_spec['name']}")
            print(f"Reason: {trigger_reason}")
            print(f"Details: {trigger_details}")
            return {"status": "completed"}
    
    orchestrator = MockOrchestrator()
    
    # Create monitor
    monitor = RuntimeMonitor(
        orchestrator,
        success_rate_threshold=0.90,  # 90% success rate minimum
        latency_threshold_ms=5000.0,  # 5 second maximum
        re_evaluation_interval_hours=24,  # Daily re-evaluation
    )
    
    # Start monitoring
    monitor.start()
    print("Monitor started - tracking runtime metrics")
    
    # Monitor will now listen for RUN_COMPLETED and RUN_FAILED events
    # and trigger re-evaluation when thresholds are violated
    
    # Get metrics
    agent_id = "test-agent"
    metrics = monitor.get_metrics(agent_id)
    if metrics:
        print(f"\nMetrics for {agent_id}:")
        print(f"  Success rate: {metrics['success_rate']:.2%}")
        print(f"  Avg latency: {metrics['avg_latency_ms']:.0f}ms")
    
    # Stop when done
    monitor.stop()
    print("\nMonitor stopped")


if __name__ == "__main__":
    main()
