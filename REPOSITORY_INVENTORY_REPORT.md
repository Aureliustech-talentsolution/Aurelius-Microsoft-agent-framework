# Aurelius Microsoft Agent Framework - Comprehensive Inventory Report

> **Generated**: January 6, 2026
> **Repository**: Aurelius-Microsoft-agent-framework
> **Analysis Method**: Multi-agent parallel assessment

---

## Executive Summary

The **Aurelius Microsoft Agent Framework** is a federally-compliant, enterprise-grade multi-language framework (Python and .NET) for building, orchestrating, and deploying AI agents. This fork of Microsoft's Agent Framework incorporates comprehensive federal compliance features including CMMC L2, NIST 800-171, and FedRAMP Moderate controls.

### Key Metrics at a Glance

| Metric | Value |
|--------|-------|
| **Total Files** | 1,768 |
| **Python Files** | 453 |
| **C# Files** | 699 |
| **Python Packages** | 9 |
| **.NET Projects** | 12 core + 17 test |
| **Samples** | 200+ |
| **CI/CD Workflows** | 16 |
| **Test Coverage Target** | 80% |
| **Documentation Files** | 138+ markdown |

---

## Table of Contents

1. [Repository Structure](#1-repository-structure)
2. [Python SDK Inventory](#2-python-sdk-inventory)
3. [.NET SDK Inventory](#3-net-sdk-inventory)
4. [Samples and Examples](#4-samples-and-examples)
5. [Testing Infrastructure](#5-testing-infrastructure)
6. [CI/CD Pipelines](#6-cicd-pipelines)
7. [Code Quality Tools](#7-code-quality-tools)
8. [External Integrations](#8-external-integrations)
9. [Federal Compliance Features](#9-federal-compliance-features)
10. [Dependencies Summary](#10-dependencies-summary)

---

## 1. Repository Structure

### Top-Level Directory Layout

```
Aurelius-Microsoft-agent-framework/
├── .aurelius/           # Aurelius-specific configurations and agents
├── .devcontainer/       # Development container configuration
├── .github/             # GitHub Actions workflows (16 workflows)
├── .vscode/             # VS Code workspace configuration
├── aurelius_agents/     # Python package for Aurelius agents
├── docs/                # Documentation and ADRs
├── dotnet/              # .NET SDK (699 C# files)
├── mlte-analysis/       # MLTE integration configuration
├── python/              # Python SDK (453 Python files)
├── tests/               # Top-level test directory
└── workflow-samples/    # Declarative workflow samples (YAML)
```

### Key Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python build and dependency configuration |
| `.pre-commit-config.yaml` | Pre-commit hooks (15+ hooks) |
| `.editorconfig` | Cross-platform code style (11KB) |
| `global.json` | .NET SDK version (9.0.300) |
| `Directory.Build.props` | .NET shared build properties |
| `.env.example` | Environment configuration template |

### Languages Distribution

| Language | File Count | Percentage |
|----------|------------|------------|
| C# | 699 | 39% |
| Python | 453 | 26% |
| Markdown | 138 | 8% |
| YAML | 70 | 4% |
| JSON | 40 | 2% |
| TOML | 12 | 1% |
| Other | 356 | 20% |

---

## 2. Python SDK Inventory

### Package Overview

**Location**: `/python/packages/`
**Build System**: UV + setuptools
**Python Requirement**: >=3.10

### Core Packages

#### 1. agent-framework-core
**Location**: `python/packages/core/`
**Files**: 60+ Python files
**Purpose**: Foundation package with all core abstractions

**Key Modules**:
| Module | Description |
|--------|-------------|
| `_agents.py` | Agent protocols and base classes |
| `_clients.py` | Chat client abstractions |
| `_tools.py` | Tool/function calling framework |
| `_memory.py` | Context providers and memory |
| `_threads.py` | Thread and message store management |
| `_middleware.py` | Middleware pipeline |
| `_workflows/` | Workflow orchestration engine (26 files) |
| `_events/` | Lifecycle event system |
| `observability.py` | OpenTelemetry integration |

**Core Dependencies**:
- `openai>=1.99.0,<2`
- `pydantic>=2,<3`
- `opentelemetry-api>=1.24`
- `mcp[ws]>=1.13`
- `azure-identity>=1,<2`

#### 2. agent-framework-a2a
**Location**: `python/packages/a2a/`
**Purpose**: Agent-to-Agent protocol communication
**Key Class**: `A2AAgent`

#### 3. agent-framework-azure-ai
**Location**: `python/packages/azure-ai/`
**Purpose**: Azure AI Foundry integration
**Key Classes**: `AzureAIAgentClient`, `AzureAISettings`

#### 4. agent-framework-copilotstudio
**Location**: `python/packages/copilotstudio/`
**Purpose**: Microsoft Copilot Studio integration
**Key Class**: `CopilotStudioAgent`

#### 5. agent-framework-mem0
**Location**: `python/packages/mem0/`
**Purpose**: Mem0 AI memory integration
**Key Class**: `Mem0Provider`

#### 6. agent-framework-redis
**Location**: `python/packages/redis/`
**Purpose**: Redis integration for message storage
**Key Classes**: `RedisChatMessageStore`, `RedisProvider`

#### 7. agent-framework-devui
**Location**: `python/packages/devui/`
**Purpose**: Debug UI with OpenAI-compatible API server
**CLI Entry Point**: `devui` command

#### 8. agent-framework-lab
**Location**: `python/packages/lab/`
**Status**: Pre-Alpha (experimental)
**Submodules**:
- `gaia/` - GAIA benchmark evaluation
- `tau2/` - TAU2 benchmark for customer support
- `lightning/` - RL training for agents

#### 9. agent-framework-mlte-integration
**Location**: `python/packages/mlte_integration/`
**Purpose**: Machine Learning Test & Evaluation with federal compliance
**Key Agents**:
- `MLTEOrchestratorAgent` - Main orchestrator
- `NegotiationAgent` - Quality Attribute Scenarios
- `TestingAgent` - Test suite execution
- `ValidationAgent` - Evidence validation
- `ReportingAgent` - Evaluation reports
- `FederalComplianceAgent` - NIST AI RMF/CMMC mapping

### Python Core Abstractions

```
Protocols (Structural Typing):
├── AgentProtocol         # Agent interface
├── ChatClientProtocol    # Chat client interface
├── ToolProtocol          # Tool interface
├── ChatMessageStoreProtocol  # Message storage interface
└── SerializationProtocol # Serialization interface

Abstract Base Classes:
├── BaseAgent             # Agent implementation base
├── BaseChatClient        # Chat client base
├── ContextProvider       # Memory/context provider
├── Middleware            # Middleware base
└── Executor              # Workflow node executor
```

---

## 3. .NET SDK Inventory

### Solution Overview

**Location**: `/dotnet/`
**Solution File**: `agent-framework-dotnet.slnx`
**SDK Version**: .NET 9.0.300
**Target Framework**: net8.0 (multi-targeting: net9.0, netstandard2.0, net472)

### Core Library Projects

#### 1. Microsoft.Agents.AI.Abstractions
**Purpose**: Foundational interfaces and abstractions
**Key Classes**:
- `AIAgent` - Abstract base for all agents
- `AgentThread` - Conversation thread abstraction
- `ChatMessageStore` - Message storage abstraction
- `AIContextProvider` - Context enhancement provider
- `AIContext` - Context container

#### 2. Microsoft.Agents.AI
**Purpose**: Core agent framework functionality
**Key Classes**:
- `ChatClientAgent` - IChatClient-based agent
- `AIAgentBuilder` - Pipeline builder for agents
- `OpenTelemetryAgent` - Telemetry wrapper
- `FunctionInvocationDelegatingAgent` - Tool execution

#### 3. Microsoft.Agents.AI.OpenAI
**Purpose**: OpenAI and Azure OpenAI integration
**Key Classes**:
- `OpenAIChatClientAgent`
- `OpenAIResponseClientAgent`

#### 4. Microsoft.Agents.AI.AzureAI
**Purpose**: Azure AI Foundry integration
**Dependencies**: `Azure.AI.Agents.Persistent`

#### 5. Microsoft.Agents.AI.CopilotStudio
**Purpose**: Microsoft Copilot Studio integration
**Dependencies**: `Microsoft.Agents.CopilotStudio.Client`

#### 6. Microsoft.Agents.AI.A2A
**Purpose**: Agent2Agent protocol support
**Key Classes**:
- `A2AAgent` - A2A client agent
- `A2AHostAgent` - A2A server host
- `A2AAgentThread` - A2A conversation thread

#### 7. Microsoft.Agents.AI.Workflows
**Purpose**: Multi-agent workflow orchestration (imperative)
**Key Components**:
- `Workflow` / `WorkflowBuilder` - Workflow definition
- `Executor` - Base executor class
- `FunctionExecutor`, `AgentExecutor`, `WorkflowExecutor`
- Edge types: `DirectEdge`, `FanInEdge`, `FanOutEdge`
- Checkpointing system

**Subdirectories**:
- `/Checkpointing` - State persistence
- `/Execution` - Workflow runtime
- `/Observability` - Telemetry
- `/Visualization` - Workflow visualization

#### 8. Microsoft.Agents.AI.Workflows.Declarative
**Purpose**: YAML/JSON declarative workflows with PowerFx
**Key Classes**:
- `DeclarativeWorkflowBuilder`
- PowerFx expression support
- Code generation (T4 templates)

#### 9. Microsoft.Agents.AI.Hosting
**Purpose**: Agent hosting infrastructure
**Key Classes**:
- `AgentCatalog` - Agent registration
- `LocalAgentRegistry` - In-process registry
- DI extensions

#### 10. Microsoft.Agents.AI.Hosting.A2A
**Purpose**: A2A protocol hosting support

#### 11. Microsoft.Agents.AI.Hosting.A2A.AspNetCore
**Purpose**: ASP.NET Core middleware for A2A

#### 12. Microsoft.Agents.AI.Hosting.OpenAI
**Purpose**: OpenAI-compatible API endpoints
**Features**: Swagger UI support

### .NET Core Abstractions

```
Core Classes:
├── AIAgent (abstract)           # Base agent class
│   ├── RunAsync()
│   ├── RunStreamingAsync()
│   ├── GetNewThread()
│   └── DeserializeThread()
├── AgentThread (abstract)       # Thread management
│   ├── MessagesReceivedAsync()
│   └── Serialize()
├── ChatMessageStore (abstract)  # Message persistence
│   ├── GetMessagesAsync()
│   └── AddMessagesAsync()
└── AIContextProvider (abstract) # Context injection
    ├── InvokingAsync()
    └── InvokedAsync()
```

---

## 4. Samples and Examples

### Sample Distribution Summary

| Category | .NET | Python |
|----------|------|--------|
| Basic Agents | 16 | 70+ |
| Agent Providers | 11 | 9 providers |
| Workflows | 25+ | 40+ |
| MCP Integration | 3 | 2 |
| Observability | 1 | 8 |
| Middleware | 1 | 8 |
| DevUI | 0 | 8 |
| Migration | 30+ | 20+ |
| **Total** | **90+** | **150+** |

### .NET Samples

**Location**: `/dotnet/samples/`

#### Getting Started - Agents (16 steps)
| Step | Topic |
|------|-------|
| Step01 | Basic agent creation |
| Step02 | Multi-turn conversation |
| Step03 | Function tools |
| Step04 | Tool approvals |
| Step05 | Structured output |
| Step06 | Persisted conversations |
| Step07 | 3rd party thread storage |
| Step08 | Observability |
| Step09 | Dependency injection |
| Step10 | As MCP tool |
| Step11 | Using images |
| Step12 | As function tool |
| Step13 | Memory |
| Step14 | Middleware |
| Step15 | Plugins |
| Step16 | Chat reduction |

#### Agent Providers (11 samples)
- Azure OpenAI (Chat, Responses, Assistants)
- OpenAI (Chat, Responses, Assistants)
- Azure AI Foundry (Agents, Models)
- A2A Protocol
- Custom Implementation
- ONNX, Ollama

#### Workflows (25+ samples)
- Foundational concepts (5 steps)
- Conditional edges (3 patterns)
- Concurrent/MapReduce
- Checkpointing (3 patterns)
- Human-in-the-loop
- Declarative with PowerFx
- Observability (Aspire, App Insights)

#### Advanced Samples
- `AgentWebChat/` - Full-stack Blazor web chat
- `A2AClientServer/` - Complete A2A demo
- `SemanticKernelMigration/` - 30+ migration samples

### Python Samples

**Location**: `/python/samples/`

#### Getting Started - Agents by Provider
| Provider | Examples |
|----------|----------|
| Azure AI Foundry | 15 |
| Azure OpenAI | 19 |
| OpenAI | 28 |
| Copilot Studio | 2 |
| Anthropic | 2 |
| Custom | 2 |
| A2A | 2 |
| Ollama | 2 |

#### Workflows (40+ samples)
- Start Here (3 foundational)
- Agents (7 samples)
- Checkpoint (3 samples)
- Composition (3 samples)
- Control-flow (6 samples)
- Human-in-the-loop (2 samples)
- Observability (1 sample)
- Orchestration (8 samples)
- Parallelism (3 samples)
- State management (1 sample)
- Visualization (1 sample)

#### Additional Categories
- Chat Client (8 examples)
- DevUI (8 examples)
- Middleware (9 examples)
- Observability (8 examples)
- Threads (3 examples)
- Context Providers - Mem0 (3), Redis (2)
- Multimodal Input (3 examples)
- MCP (2 examples)
- Evaluation/Red Team (1 comprehensive)

### Declarative Workflows

**Location**: `/workflow-samples/`
- `DeepResearch.yaml`
- `HumanInLoop.yaml`
- `Marketing.yaml`
- `MathChat.yaml`

---

## 5. Testing Infrastructure

### Test Framework Summary

| Aspect | Python | .NET |
|--------|--------|------|
| **Framework** | pytest 8.4.1+ | xUnit 2.6.6 |
| **Coverage** | pytest-cov | coverlet |
| **Mocking** | pytest-mock | NSubstitute, Moq |
| **Async** | pytest-asyncio | Built-in |
| **Parallel** | pytest-xdist | xUnit parallel |
| **Assertions** | Built-in | FluentAssertions |

### Test Project Counts

| Category | Python | .NET |
|----------|--------|------|
| Unit Tests | 80+ files | 10 projects |
| Integration Tests | Included | 7 projects |
| Sample Tests | 10+ files | Included |
| **Total** | **90+ files** | **17 projects** |

### Python Test Structure
```
python/
├── tests/
│   ├── unit/
│   └── samples/
└── packages/
    ├── core/tests/
    ├── a2a/tests/
    ├── azure-ai/tests/
    ├── copilotstudio/tests/
    ├── devui/tests/
    ├── mem0/tests/
    ├── redis/tests/
    └── mlte_integration/tests/
```

### .NET Test Structure
```
dotnet/tests/
├── Microsoft.Agents.AI.UnitTests/
├── Microsoft.Agents.AI.Abstractions.UnitTests/
├── Microsoft.Agents.AI.A2A.UnitTests/
├── Microsoft.Agents.AI.AzureAI.UnitTests/
├── Microsoft.Agents.AI.OpenAI.UnitTests/
├── Microsoft.Agents.AI.Workflows.UnitTests/
├── Microsoft.Agents.AI.Hosting.UnitTests/
├── OpenAIChatCompletion.IntegrationTests/
├── OpenAIAssistant.IntegrationTests/
├── OpenAIResponse.IntegrationTests/
├── AzureAIAgentsPersistent.IntegrationTests/
├── CopilotStudio.IntegrationTests/
└── AgentConformance.IntegrationTests/
```

### Coverage Requirements
- **Target**: 80% minimum
- **Branch Coverage**: Required
- **Enforcement**: CI pipeline gates

---

## 6. CI/CD Pipelines

### GitHub Actions Workflows (16 total)

#### Python Workflows (8)
| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `python-tests.yml` | PR | Matrix testing (3.10-3.13) |
| `python-test-coverage.yml` | PR | Coverage analysis |
| `python-test-coverage-report.yml` | Post-coverage | PR comments |
| `python-merge-tests.yml` | Merge queue | Integration tests |
| `python-code-quality.yml` | PR | Static analysis |
| `python-lab-tests.yml` | PR (lab/**) | Experimental tests |
| `python-release.yml` | Release | Package publishing |
| `python-docs.yml` | Manual | Documentation |

#### .NET Workflows (4)
| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `dotnet-build-and-test.yml` | PR/Merge | Build + test matrix |
| `dotnet-format.yml` | PR | Code formatting |
| `codeql-analysis.yml` | Push/Schedule | Security scanning |
| `dotnet-check-coverage.ps1` | In workflow | Coverage validation |

#### Cross-Platform Workflows (4)
| Workflow | Purpose |
|----------|---------|
| `ci.yaml` | Comprehensive CI (Aurelius custom) |
| `merge-gatekeeper.yml` | PR validation |
| `markdown-link-check.yml` | Documentation validation |
| `label-*.yml` (3) | Repository automation |

### CI Pipeline Features
- **Multi-OS Matrix**: Ubuntu, Windows
- **Multi-Version Matrix**: Python 3.10-3.13, .NET 8.0/9.0
- **Coverage Enforcement**: 80% threshold
- **Security Scanning**: CodeQL, Bandit, Semgrep
- **SBOM Generation**: CycloneDX format
- **Integration Testing**: Azure, OpenAI providers

---

## 7. Code Quality Tools

### Python Quality Stack

| Category | Tools |
|----------|-------|
| **Linting** | Ruff (replaces flake8, pylint, isort) |
| **Formatting** | Black, isort |
| **Type Checking** | MyPy (strict), Pyright (strict) |
| **Security** | Bandit, Semgrep, Safety, pip-audit |
| **Testing** | pytest + extensions |
| **Pre-commit** | 15+ hooks configured |

#### Pre-commit Hooks
```yaml
- check-toml, check-yaml, check-json
- end-of-file-fixer
- mixed-line-ending
- check-ast (Python syntax)
- nbqa-check-ast (Jupyter)
- pyupgrade (Python 3.10+)
- black, isort, ruff
- mypy, pyright
- bandit (security)
```

### .NET Quality Stack

| Category | Tools |
|----------|-------|
| **Analyzers** | Microsoft.CodeAnalysis.NetAnalyzers |
| **Style** | StyleCop.Analyzers |
| **Security** | SecurityCodeScan |
| **Testing** | xUnit, FluentAssertions |
| **Coverage** | coverlet, ReportGenerator |

#### Security Rules Enforced (as errors)
- SCS0005: Weak random number generator
- SCS0006: Weak hashing
- SCS0007: XXE injection
- SCS0014: SQL injection
- SCS0015: Hardcoded passwords
- SCS0018: Path traversal
- SCS0020: Weak cipher
- SCS0029: XSS
- SCS0030: Insecure deserialization

---

## 8. External Integrations

### AI Provider Integrations

| Provider | Python | .NET |
|----------|--------|------|
| Azure OpenAI | ✅ | ✅ |
| OpenAI | ✅ | ✅ |
| Azure AI Foundry | ✅ | ✅ |
| Anthropic | ✅ | ✅ |
| Ollama | ✅ | ✅ |
| AWS Bedrock | - | ✅ |
| ONNX Runtime | - | ✅ |

### Protocol Integrations

| Protocol | Python | .NET |
|----------|--------|------|
| A2A (Agent-to-Agent) | ✅ | ✅ |
| MCP (Model Context Protocol) | ✅ | ✅ |
| OpenAI Assistants API | ✅ | ✅ |
| OpenAI Responses API | ✅ | ✅ |

### Memory & Storage

| Service | Python | .NET |
|---------|--------|------|
| Redis | ✅ | - |
| Mem0 AI | ✅ | - |
| In-Memory | ✅ | ✅ |
| Custom Storage | ✅ | ✅ |

### Azure Services

| Service | Purpose |
|---------|---------|
| Azure OpenAI | LLM inference |
| Azure AI Foundry | Agent hosting |
| Azure Key Vault | Secrets management |
| Azure Monitor | Observability |
| Azure Cosmos DB | Audit logging |
| Azure Cache for Redis | State storage |
| Azure Kubernetes Service | Deployment |

### Observability

| Platform | Python | .NET |
|----------|--------|------|
| OpenTelemetry | ✅ | ✅ |
| Azure Monitor | ✅ | ✅ |
| Aspire Dashboard | - | ✅ |
| Console Export | ✅ | ✅ |

---

## 9. Federal Compliance Features

### Compliance Standards Supported

| Standard | Status |
|----------|--------|
| CMMC Level 2 | All 110 practices |
| NIST 800-171 Rev 2 | Full compliance |
| FedRAMP Moderate | Baseline controls |
| NIST AI RMF | Integrated |
| SSDF | Framework aligned |

### Security Architecture

| Feature | Implementation |
|---------|----------------|
| Authentication | PIV/CAC, Entra ID |
| Encryption | TLS 1.3, AES-256-GCM |
| Key Management | Azure Key Vault |
| Zero Trust | Network segmentation |
| Audit Logging | Immutable, 10-year retention |
| SBOM | CycloneDX format |
| Vulnerability SLA | 24-hour remediation |

### MLTE Integration

**Machine Learning Test & Evaluation framework** for:
- Quality Attribute Scenarios (QAS)
- Evidence-based validation
- Federal compliance mapping
- OSCAL export

### Compliance Automation

| Check | Timing |
|-------|--------|
| Secrets detection | Pre-commit |
| Security scanning | CI pipeline |
| License compliance | Pre-merge |
| SBOM generation | Release |
| Vulnerability scan | Daily |

---

## 10. Dependencies Summary

### Python Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| openai | >=1.99.0,<2 | OpenAI client |
| pydantic | >=2,<3 | Data validation |
| azure-identity | >=1,<2 | Azure auth |
| opentelemetry-api | >=1.24 | Telemetry |
| mcp[ws] | >=1.13 | MCP support |
| fastapi | >=0.104.0 | DevUI server |
| redis | >=6.4.0 | State storage |
| mem0ai | >=0.1.117 | Memory service |
| mlte | >=2.2.0 | Evaluation |

### .NET Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Microsoft.Extensions.AI | 9.9.1 | AI abstractions |
| Azure.AI.OpenAI | 2.5.0-beta.1 | Azure OpenAI |
| OpenAI | 2.5.0 | OpenAI client |
| A2A | 0.3.1-preview | A2A protocol |
| ModelContextProtocol | 0.4.0-preview.2 | MCP support |
| OpenTelemetry | 1.12.0 | Telemetry |
| Azure.Identity | 1.17.0 | Azure auth |
| Microsoft.SemanticKernel | 1.66.0 | SK integration |

### Development Dependencies

| Tool | Python Version | .NET Version |
|------|----------------|--------------|
| Test Framework | pytest 8.4.1+ | xUnit 2.6.6 |
| Linter | ruff 0.11.8+ | StyleCop 1.2.0 |
| Type Checker | mypy 1.16.1+ | Built-in |
| Coverage | pytest-cov 6.2.1+ | coverlet 6.0.0 |
| Security | bandit 1.8.5 | SecurityCodeScan 5.6.7 |

---

## Appendix A: File Statistics

### By File Type

| Extension | Count | Size |
|-----------|-------|------|
| .cs | 699 | ~2.5 MB |
| .py | 453 | ~1.8 MB |
| .md | 138 | ~800 KB |
| .yaml/.yml | 70 | ~150 KB |
| .json | 40 | ~100 KB |
| .csproj | 123 | ~200 KB |
| .toml | 12 | ~50 KB |

### By Directory

| Directory | Files | Purpose |
|-----------|-------|---------|
| /dotnet/src | 382 | .NET source |
| /dotnet/tests | 250 | .NET tests |
| /dotnet/samples | 60 | .NET samples |
| /python/packages | 237 | Python packages |
| /python/samples | 150 | Python samples |
| /python/tests | 40 | Python tests |
| /.github | 50 | CI/CD config |
| /docs | 30 | Documentation |

---

## Appendix B: Architecture Decision Records (ADRs)

| ADR | Title |
|-----|-------|
| 0001 | Agent Run Response |
| 0002 | Agent Tools |
| 0003 | Agent OpenTelemetry Instrumentation |
| 0004 | Foundry SDK Extensions |
| 0005 | Python Naming Conventions |
| 0006 | User Approval |
| 0007 | Agent Filtering Middleware |
| 0007 | Python Subpackages |

---

## Appendix C: Quick Reference

### Python Quick Start
```bash
# Install
pip install agent-framework-core

# Basic agent
from agent_framework import ChatAgent, OpenAIChatClient
agent = ChatAgent(client=OpenAIChatClient(model="gpt-4"))
response = await agent.run("Hello!")
```

### .NET Quick Start
```bash
# Install
dotnet add package Microsoft.Agents.AI
```

```csharp
// Basic agent
var agent = new OpenAIChatClientAgent(client, "gpt-4");
var thread = agent.GetNewThread();
var response = await agent.RunAsync(thread, "Hello!");
```

### DevUI Launch
```bash
cd python/samples/getting_started/devui/agents/weather_agent_azure
devui
```

---

*Report generated by multi-agent parallel assessment. Last updated: January 6, 2026.*
