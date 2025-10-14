"""Example: Using MLTEEvaluationMiddleware."""

from mlte_integration.middleware import MLTEEvaluationMiddleware, EvaluationMode


def main():
    """Demonstrate middleware usage."""
    # Mock orchestrator (replace with real one)
    class MockOrchestrator:
        async def run(self, agent_spec):
            print(f"Evaluating agent: {agent_spec['name']}")
            return {"status": "completed"}
    
    orchestrator = MockOrchestrator()
    
    # Create middleware
    middleware = MLTEEvaluationMiddleware(
        orchestrator,
        mode=EvaluationMode.ASYNCHRONOUS,
        trigger_on_create=True,
        trigger_on_first_run=True,
        trigger_on_update=True,
    )
    
    # Start listening
    middleware.start()
    print("Middleware started - listening for events")
    
    # Now when agents are created/updated, evaluation will trigger automatically
    # Example: agent_framework will emit CREATED event -> middleware triggers evaluation
    
    # Check status
    print(f"Running: {middleware.is_running()}")
    print(f"Evaluated agents: {len(middleware.get_evaluated_agents())}")
    
    # Stop when done
    middleware.stop()
    print("Middleware stopped")


if __name__ == "__main__":
    main()
