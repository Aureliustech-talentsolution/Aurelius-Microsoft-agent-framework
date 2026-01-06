# AGENT.md - AI Assistant Instructions for Microsoft Agent Framework

This file provides workspace-specific instructions for AI coding assistants (Claude, Copilot, Cursor, etc.) working on the Microsoft Agent Framework repository.

---

## Project Overview

**Microsoft Agent Framework** is a multi-language framework for building, orchestrating, and deploying AI agents with support for both Python and .NET implementations.

**Repository Structure:**
```
├── python/                  # Python implementation (primary)
│   ├── packages/           # 9 independent packages (core, azure-ai, a2a, etc.)
│   ├── samples/            # Code examples and tutorials
│   └── tests/              # Integration tests
├── dotnet/                  # .NET/C# implementation
│   ├── src/                # 16+ projects
│   ├── samples/            # .NET examples
│   └── tests/              # .NET tests
├── docs/                    # Documentation, ADRs, specs
├── .aurelius/               # Aurelius compliance/security configs
└── .github/workflows/       # CI/CD (18+ workflows)
```

---

## Python Development

### Environment Setup
```bash
cd python
python -m venv .venv && source .venv/bin/activate
pip install uv
uv sync --all-packages --all-extras --dev -U
pre-commit install
pre-commit install --hook-type commit-msg
```

### Package Manager
**Always use `uv`**, not `pip` directly:
```bash
uv sync --all-packages    # Install all workspace packages
uv add <package>          # Add dependency
uv run <command>          # Run in venv context
```

### Code Quality Commands
```bash
poe fmt                   # Format code (Ruff)
poe lint                  # Lint code (Ruff)
poe mypy                  # Type check (MyPy strict)
poe pyright               # Type check (Pyright strict)
poe all-tests             # Run all tests with coverage
poe check                 # Run all of the above
```

### Testing
```bash
pytest packages/**/tests              # All package tests
pytest packages/core/tests -v         # Specific package
poe all-tests-cov                     # With coverage reports
```

**Coverage requirement: 80% minimum (enforced in CI)**

### Package Structure
Each package in `python/packages/`:
- Extends root `pyproject.toml` config
- Has own `poe` tasks: `poe fmt`, `poe lint`, `poe test`, `poe mypy`
- Uses Flit as build backend
- Follows naming: `agent_framework_<name>`

---

## .NET Development

### Build Commands
```bash
dotnet build dotnet/agent-framework-dotnet.slnx
dotnet test dotnet/agent-framework-dotnet.slnx
dotnet build -c Release
```

### Target Frameworks
- **Primary**: `net8.0`
- **Legacy support**: `net472`

### Key Settings (Directory.Build.props)
- `TreatWarningsAsErrors=true`
- `Nullable=enable`
- `EnforceCodeStyleInBuild=true`
- `AnalysisMode=All`

---

## Coding Conventions

### Python

**Type Hints (REQUIRED - Strict Mode)**
```python
# Always use type hints
def process(data: str, count: int = 0) -> list[str]:
    ...

# Use union syntax (not Optional)
value: str | None = None

# Async functions
async def fetch(url: str) -> dict[str, Any]:
    ...
```

**Imports**
```python
# isort profile: black
# Order: stdlib, third-party, local
from __future__ import annotations

import asyncio
from typing import Any

from pydantic import BaseModel

from agent_framework import ChatAgent
```

**Docstrings (Google Style)**
```python
def create_agent(name: str, instructions: str) -> ChatAgent:
    """Create a new chat agent.

    Args:
        name: The agent's display name.
        instructions: System prompt for the agent.

    Returns:
        Configured ChatAgent instance.

    Raises:
        ValueError: If name is empty.
    """
```

**Pydantic Models**
```python
from pydantic import BaseModel, Field, ConfigDict

class AgentConfig(BaseModel):
    """Configuration for an agent."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
```

**Async Patterns**
```python
# Use async context managers
async with AsyncExitStack() as stack:
    client = await stack.enter_async_context(create_client())

# Async generators for streaming
async def stream_responses() -> AsyncIterable[str]:
    async for chunk in response:
        yield chunk.content
```

### C#/.NET

**Naming Conventions (Enforced)**
- Async methods: `*Async` suffix (e.g., `RunAsync`)
- Interfaces: `I*` prefix (e.g., `IAgent`)
- Private fields: `_camelCase` (e.g., `_client`)
- Types/Methods: `PascalCase`

**Example Pattern**
```csharp
public class ChatAgent : IAgent
{
    private readonly IChatClient _client;

    public async Task<string> RunAsync(string prompt, CancellationToken ct = default)
    {
        return await _client.SendAsync(prompt, ct);
    }
}
```

---

## Architecture Patterns

### Agent Protocol (Python)
```python
@runtime_checkable
class AgentProtocol(Protocol):
    @property
    def id(self) -> str: ...

    @property
    def name(self) -> str | None: ...

    async def run(
        self,
        messages: str | ChatMessage | list[ChatMessage],
        *,
        thread: AgentThread | None = None,
    ) -> AgentRunResponse: ...
```

### Middleware Pattern
```python
class LoggingMiddleware:
    async def __call__(
        self,
        context: MiddlewareContext,
        next_handler: Callable,
    ) -> Any:
        logger.info(f"Request: {context.request}")
        result = await next_handler(context)
        logger.info(f"Response: {result}")
        return result
```

### Observability (OpenTelemetry)
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def process_request(request: Request) -> Response:
    with tracer.start_as_current_span("process_request") as span:
        span.set_attribute("request.id", request.id)
        return await handle(request)
```

---

## Testing Patterns

### Python Test Structure
```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_agent_run():
    """Test agent run with mocked client."""
    mock_client = AsyncMock()
    mock_client.send.return_value = "response"

    agent = ChatAgent(client=mock_client)
    result = await agent.run("hello")

    assert result.content == "response"
    mock_client.send.assert_called_once()

@pytest.mark.azure
async def test_azure_integration():
    """Test with Azure provider (skipped without credentials)."""
    ...

# Use fixtures from conftest.py
def test_with_fixtures(agent_thread, chat_client):
    ...
```

### Test Markers
```python
@pytest.mark.azure      # Azure provider tests
@pytest.mark.azure_ai   # Azure AI tests
@pytest.mark.openai     # OpenAI provider tests
```

---

## Security & Compliance

### Pre-commit Hooks (REQUIRED)
All commits are checked for:
- Secrets detection (CMMC SC.3.177)
- Security vulnerabilities (Bandit, Safety)
- Code formatting and linting
- Conventional commit messages

### Security Rules (.editorconfig - C#)
These are **ERRORS**, not warnings:
- `SCS0005` - Weak random
- `SCS0006` - Weak hashing
- `SCS0014` - SQL injection
- `SCS0015` - Hardcoded password
- `SCS0029` - XSS
- `SCS0030` - Insecure deserialization

### Never Commit
- API keys, tokens, credentials
- `.env` files with secrets
- Private keys or certificates

---

## Common Tasks

### Adding a New Python Package
1. Create `python/packages/<name>/` with:
   - `pyproject.toml` (extend root config)
   - `agent_framework_<name>/__init__.py`
   - `tests/`
2. Add to workspace in root `pyproject.toml`
3. Run `uv sync --all-packages`

### Adding a Tool/Function
```python
from agent_framework import tool

@tool
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database for matching records.

    Args:
        query: Search query string.
        limit: Maximum results to return.

    Returns:
        List of matching records.
    """
    return db.search(query, limit=limit)
```

### Creating a Workflow
```python
from agent_framework.workflows import Workflow, step

@step
async def analyze(data: str) -> dict:
    ...

@step
async def summarize(analysis: dict) -> str:
    ...

workflow = Workflow([analyze, summarize])
result = await workflow.run(data="input")
```

---

## CI/CD Requirements

### Pull Request Checks
All PRs must pass:
1. **Python**: Ruff lint/format, MyPy, Pyright, pytest (80% coverage)
2. **.NET**: Build (Release), tests, analyzers
3. **Security**: CodeQL, secret scanning
4. **Docs**: Markdownlint

### Branch Strategy
- `main` - Protected, requires PR
- Feature branches from `main`
- Squash merge preferred

---

## File Locations Quick Reference

| What | Where |
|------|-------|
| Python packages | `python/packages/` |
| Python samples | `python/samples/getting_started/` |
| .NET source | `dotnet/src/` |
| .NET samples | `dotnet/samples/GettingStarted/` |
| ADRs | `docs/decisions/` |
| Design docs | `docs/design/` |
| CI workflows | `.github/workflows/` |
| Pre-commit config | `.pre-commit-config.yaml` |
| Python config | `python/pyproject.toml` |
| .NET build props | `Directory.Build.props` |

---

## Best Practices Reference

For comprehensive AI agent development best practices, see:
- **[docs/AI_AGENT_BEST_PRACTICES.md](./docs/AI_AGENT_BEST_PRACTICES.md)** - Bleeding-edge research and patterns

For framework-specific skills guide:
- **[MICROSOFT_AGENT_FRAMEWORK_SKILLS.md](./MICROSOFT_AGENT_FRAMEWORK_SKILLS.md)** - SME-level production guide

---

**Last Updated**: January 2026
