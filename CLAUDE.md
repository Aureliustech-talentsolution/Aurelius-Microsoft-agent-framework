# CLAUDE.md - Microsoft Agent Framework

Workspace-specific instructions for Claude Code working on this repository.

---

## Project Context

**Microsoft Agent Framework** - Multi-language framework for building, orchestrating, and deploying AI agents. Supports Python and .NET with graph-based workflows, tool integration, and OpenTelemetry observability.

**Repository**: Aurelius fork for federal compliance (CMMC/NIST aligned)

---

## Tech Stack

**Python** (primary)
- Python 3.10+ required
- Package manager: `uv` (NOT pip directly)
- Build backend: Flit
- Type checking: MyPy + Pyright (both strict)
- Linting/Formatting: Ruff (replaces Black, isort, Flake8)
- Testing: pytest with 80% coverage minimum

**.NET**
- Target frameworks: `net8.0` (primary), `net472` (legacy)
- Build settings: `TreatWarningsAsErrors=true`, `Nullable=enable`
- Analyzers: `AnalysisMode=All`, `EnforceCodeStyleInBuild=true`

---

## Key Directories

```
python/packages/          # 9 independent Python packages
python/samples/           # Python code examples
python/tests/             # Integration tests
dotnet/src/               # 16+ .NET projects
dotnet/samples/           # .NET examples
docs/decisions/           # ADRs
docs/design/              # Design documents
.aurelius/                # Compliance/security configs
.github/workflows/        # CI/CD (18+ workflows)
```

---

## Essential Commands

### Python Setup
```bash
cd python
python -m venv .venv && source .venv/bin/activate
pip install uv
uv sync --all-packages --all-extras --dev -U
pre-commit install && pre-commit install --hook-type commit-msg
```

### Python Development
```bash
poe fmt                   # Format (Ruff)
poe lint                  # Lint (Ruff)
poe mypy                  # Type check (MyPy strict)
poe pyright               # Type check (Pyright strict)
poe all-tests             # All tests with coverage
poe check                 # Run ALL checks (fmt, lint, mypy, pyright, tests)
```

### .NET Development
```bash
dotnet build dotnet/agent-framework-dotnet.slnx
dotnet test dotnet/agent-framework-dotnet.slnx
dotnet build -c Release
```

---

## Code Conventions

### Python - Required Patterns
```python
# ALWAYS use type hints (MyPy/Pyright strict mode)
def process(data: str, count: int = 0) -> list[str]: ...

# Use union syntax, NOT Optional
value: str | None = None

# Async context managers for resource management
async with AsyncExitStack() as stack:
    client = await stack.enter_async_context(create_client())

# Google-style docstrings with Args, Returns, Raises
def create_agent(name: str) -> ChatAgent:
    """Create a new chat agent.

    Args:
        name: The agent's display name.

    Returns:
        Configured ChatAgent instance.

    Raises:
        ValueError: If name is empty.
    """
```

### Python - Import Order (isort black profile)
```python
from __future__ import annotations

import asyncio                    # stdlib
from typing import Any

from pydantic import BaseModel    # third-party

from agent_framework import X     # local
```

### .NET - Required Patterns
```csharp
// Async methods: *Async suffix
public async Task<string> RunAsync(string prompt, CancellationToken ct = default)

// Interfaces: I* prefix
public interface IAgent { }

// Private fields: _camelCase
private readonly IChatClient _client;
```

---

## Testing Requirements

### Python
```bash
pytest packages/**/tests              # All package tests
pytest packages/core/tests -v         # Single package
poe all-tests-cov                     # With coverage reports
```

**Markers:**
- `@pytest.mark.azure` - Azure provider tests
- `@pytest.mark.azure_ai` - Azure AI tests
- `@pytest.mark.openai` - OpenAI provider tests

**Coverage:** 80% minimum (CI enforced)

### .NET
```bash
dotnet test dotnet/agent-framework-dotnet.slnx --verbosity normal
```

---

## Security Guidelines

### Pre-commit Hooks (REQUIRED)
All commits checked for:
- Secrets detection (CMMC SC.3.177)
- Security vulnerabilities (Bandit, Safety)
- Code formatting and linting
- Conventional commit messages

### Never Commit
- API keys, tokens, credentials
- `.env` files with secrets
- Private keys or certificates

### C# Security Errors (.editorconfig enforced)
These are ERRORS, not warnings:
- `SCS0005` - Weak random
- `SCS0006` - Weak hashing
- `SCS0014` - SQL injection
- `SCS0015` - Hardcoded password
- `SCS0029` - XSS
- `SCS0030` - Insecure deserialization

---

## Extended Thinking

Use extended thinking for complex tasks in this codebase:

**When to use:**
- Multi-file refactoring across Python/C# boundaries
- Architecture decisions affecting workflow orchestration
- Security analysis and compliance verification
- Complex async patterns with middleware chains

**Activation:** "think", "think harder", or "ultrathink"

**Token budget guidance:**
- Simple tasks: Skip extended thinking
- Moderate complexity: 1,024-4,096 tokens
- Complex architecture: 8,192-16,384 tokens
- Deep security analysis: 16,384+ tokens

---

## Context Management

### This Repository's Structure
- Keep focused on current task directory (python/ OR dotnet/)
- Cross-language changes require explicit coordination
- Reference `/docs/decisions/` for ADRs before architectural changes

### Memory Strategy
- Store learned patterns in session notes
- Reference `AGENT.md` for workspace conventions
- Reference `MICROSOFT_AGENT_FRAMEWORK_SKILLS.md` for SME patterns
- Reference `docs/AI_AGENT_BEST_PRACTICES.md` for bleeding-edge approaches

### Token Efficiency
- Don't read entire packages; target specific files
- Use `@filename.md` sparingly
- Batch related file reads in single operations

---

## Common Patterns

### Adding a Python Package
1. Create `python/packages/<name>/` with:
   - `pyproject.toml` (extend root config)
   - `agent_framework_<name>/__init__.py`
   - `tests/`
2. Add to workspace in root `pyproject.toml`
3. Run `uv sync --all-packages`

### Creating a Tool/Function
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
async def analyze(data: str) -> dict: ...

@step
async def summarize(analysis: dict) -> str: ...

workflow = Workflow([analyze, summarize])
result = await workflow.run(data="input")
```

### Agent Protocol Implementation
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

---

## Decision Framework

Before making changes:
1. **DOING**: State intended action
2. **EXPECT**: Predict the outcome
3. **VERIFY**: Confirm after execution
4. **DIVERGE**: If unexpected, explain and ask

Max 3 actions before verifying. Never hide confusion.

---

## File Locations Reference

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

## Related Documentation

- **[AGENT.md](./AGENT.md)** - General AI assistant instructions
- **[MICROSOFT_AGENT_FRAMEWORK_SKILLS.md](./MICROSOFT_AGENT_FRAMEWORK_SKILLS.md)** - SME production guide
- **[docs/AI_AGENT_BEST_PRACTICES.md](./docs/AI_AGENT_BEST_PRACTICES.md)** - Bleeding-edge research

---

**Last Updated**: January 2026
