"""
Pytest configuration and fixtures for Aurelius Agent Framework tests
"""

import os
from typing import Any, Generator

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def deployment_environment() -> str:
    """Get deployment environment."""
    return os.getenv("DEPLOYMENT_ENVIRONMENT", "test")


@pytest.fixture(scope="session")
def is_ci_environment() -> bool:
    """Check if running in CI environment."""
    return os.getenv("CI", "false").lower() == "true"


@pytest.fixture(scope="session")
def skip_integration_in_ci(is_ci_environment: bool) -> Generator[None, None, None]:
    """Skip integration tests in CI unless explicitly enabled."""
    if is_ci_environment and os.getenv("RUN_INTEGRATION_TESTS", "false").lower() != "true":
        pytest.skip("Integration tests disabled in CI")
    yield


@pytest.fixture(scope="session")
def azure_credentials() -> dict[str, Any]:
    """Get Azure credentials for testing."""
    return {
        "tenant_id": os.getenv("AZURE_TENANT_ID"),
        "client_id": os.getenv("AZURE_CLIENT_ID"),
        "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
    }


@pytest.fixture(scope="function")
def mock_agent():
    """Mock agent for testing."""
    from unittest.mock import AsyncMock, MagicMock

    agent = MagicMock()
    agent.run = AsyncMock(return_value="Mock response")
    agent.id = "test-agent-123"
    agent.name = "TestAgent"
    return agent


@pytest.fixture(scope="function")
def sample_cui_data() -> dict[str, str]:
    """Sample CUI data for testing."""
    return {
        "classification": "CUI",
        "content": "This is controlled unclassified information",
        "marking": "CONTROLLED UNCLASSIFIED INFORMATION",
    }


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "security: Security tests")
    config.addinivalue_line("markers", "compliance: Compliance tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
