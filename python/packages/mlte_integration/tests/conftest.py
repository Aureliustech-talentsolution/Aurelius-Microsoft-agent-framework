"""
Pytest configuration and fixtures for MLTE integration tests.

Federal Compliance: Test infrastructure supports CMMC L2 audit requirements.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
import yaml


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_yaml(temp_dir: Path) -> Path:
    """Create a sample YAML configuration file."""
    config_data = {
        "mlte": {
            "store": {
                "uri": "fs://./test-mlte-store",
                "type": "filesystem",
                "connection_pool_size": 5,
            },
            "evaluation_enabled": True,
            "evaluation_mode": "synchronous",
            "fail_on_error": False,
            "quality_gates": {
                "accuracy_min": 0.90,
                "security_min": 0.85,
                "latency_max_ms": 3000,
                "memory_max_mb": 256,
            },
            "orchestrator": {
                "parallel_execution": True,
                "max_workers": 2,
                "timeout_seconds": 120,
            },
            "agents": {
                "negotiation": {
                    "llm_model": "gpt-3.5-turbo",
                    "temperature": 0.5,
                    "max_tokens": 2048,
                    "timeout_seconds": 30,
                }
            },
            "federal_compliance": {
                "enabled": True,
                "standards": ["NIST AI RMF", "CMMC L2"],
                "oscal_export": True,
                "audit_trail": True,
                "classification": "CUI",
            },
        }
    }

    config_path = temp_dir / "test-config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config_data, f)

    return config_path


@pytest.fixture
def sample_env_vars() -> Generator[None, None, None]:
    """Set sample environment variables for testing."""
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["MLTE_STORE_URI"] = "fs://./test-store"
    os.environ["MLTE_ENABLE_EVALUATION"] = "true"
    os.environ["MLTE_EVALUATION_MODE"] = "asynchronous"
    os.environ["MLTE_FAIL_ON_ERROR"] = "true"
    os.environ["ENABLE_FEDERAL_COMPLIANCE_AGENT"] = "true"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_agent_spec():
    """Create a sample AgentSpec for testing."""
    from agent_framework_mlte_integration.types import AgentSpec

    return AgentSpec(
        model_id="test_agent",
        version="1.0.0",
        name="Test Agent",
        description="A test agent for MLTE evaluation",
        instructions="You are a helpful test assistant.",
        tools=[
            {
                "name": "search",
                "description": "Search for information",
                "parameters": {"query": "string"},
            }
        ],
        agent_type="ChatAgent",
        metadata={"environment": "test", "team": "mlte-dev"},
    )


@pytest.fixture
def sample_quality_gate():
    """Create a sample QualityGate for testing."""
    from agent_framework_mlte_integration.types import QualityGate

    return QualityGate(
        name="Minimum Accuracy",
        test_case_id="accuracy",
        threshold=0.95,
        comparison=">=",
        severity="critical",
        blocking=True,
        description="Agent must meet minimum accuracy threshold",
        metadata={"category": "performance"},
    )
