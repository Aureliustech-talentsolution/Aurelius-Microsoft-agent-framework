# Project-Specific CLAUDE.md
# Microsoft Agent Framework - Aurelius Implementation

This file contains project-specific instructions that **OVERRIDE** the global CLAUDE.md defaults.

---

## Project Context

**Repository**: https://github.com/AureliustechandTalentSolutions/Microsoft-agent-framework
**Primary Purpose**: Federally-compliant implementation of Microsoft Agent Framework
**Key Technologies**: Python 3.10+, .NET 8.0+, Azure OpenAI, Azure AI Foundry
**Compliance Requirements**: CMMC L2, NIST 800-171, FedRAMP Moderate

---

## Project-Specific Overrides

### Language Preferences
```yaml
default_language: python  # Primary
secondary_language: dotnet  # For enterprise scenarios
prefer_python_for:
  - Agent development
  - Workflow orchestration
  - Rapid prototyping
prefer_dotnet_for:
  - Enterprise integrations
  - Windows-based deployments
  - Power Platform connectors
```

### Build Commands (Override Global)
```yaml
python:
  install: "uv pip install -e .[all]"
  test: "pytest --cov --cov-report=html --cov-report=term"
  lint: "ruff check . && black --check . && isort --check ."
  format: "ruff check --fix . && black . && isort ."
  typecheck: "mypy . && pyright ."
  security: "bandit -r . && semgrep --config=auto && safety check && pip-audit"

dotnet:
  restore: "dotnet restore"
  build: "dotnet build --no-restore"
  test: "dotnet test --no-build --verbosity normal --collect:\"XPlat Code Coverage\""
  publish: "dotnet publish -c Release"
```

### Testing Standards (Stricter than Global)
```yaml
coverage_threshold_pct: 85  # Higher than global 80%
mutation_threshold_pct: 65  # Higher than global 60%
integration_test_required: true
security_test_required: true
compliance_test_required: true
```

### Evidence Requirements (Enhanced)
```yaml
always_generate:
  - SBOM (CycloneDX format)
  - License compliance report
  - Security scan results (Bandit, Semgrep, Safety, pip-audit)
  - Test coverage report (HTML + JSON)
  - Mutation testing report
  - Static analysis report (Ruff, MyPy, Pyright)
  - OpenTelemetry traces (for runtime behavior)
  - Compliance checklist (CMMC L2 controls)

evidence_location: .aurelius/evidence/
retention_period: 7_years  # Federal requirement
```

---

## Microsoft Agent Framework Specifics

### Core Packages
```yaml
python_packages:
  core:
    - agent-framework-core
    - agent-framework-azure-ai
    - agent-framework-openai
    - agent-framework-mem0
    - agent-framework-redis

  optional:
    - agent-framework-devui
    - agent-framework-a2a
    - agent-framework-copilotstudio
    - agent-framework-lab

dotnet_packages:
  - Microsoft.Agents.AI
  - Microsoft.Agents.AI.OpenAI
  - Microsoft.Agents.AI.AzureFoundry
  - Microsoft.Agents.Workflows
```

### Common Patterns to Reference
```yaml
agent_creation:
  python: "python/samples/getting_started/agents/"
  dotnet: "dotnet/samples/GettingStarted/Agents/"

workflow_orchestration:
  python: "python/samples/getting_started/workflows/"
  dotnet: "dotnet/samples/GettingStarted/Workflows/"

mcp_integration:
  python: "python/samples/getting_started/mcp/"
  dotnet: "dotnet/samples/GettingStarted/ModelContextProtocol/"

devui_usage:
  python: "python/packages/devui/samples/"
```

### Architecture Decision Records
When making architectural decisions, create ADR in:
- Location: `docs/decisions/NNNN-decision-name.md`
- Template: `docs/decisions/adr-template.md`
- Format: Standard ADR with Status, Context, Decision, Consequences

---

## Federal Compliance Workflow

### Before Every Task Start
1. **Classify Data**: Determine if CUI/FOUO handling required
2. **Review Controls**: Check applicable CMMC/NIST controls
3. **Evidence Plan**: Identify what evidence artifacts needed
4. **Security Review**: Consider security implications

### During Implementation
1. **Security-First Coding**: Never hardcode secrets, validate inputs
2. **Audit Logging**: Log all security-relevant events
3. **Documentation**: Document security controls as implemented
4. **Testing**: Include security and compliance test cases

### After Implementation
1. **Security Scan**: Run all security tools (Bandit, Semgrep, Safety)
2. **Generate Evidence**: Create SBOMs, test reports, compliance docs
3. **Peer Review**: Require security-aware code review
4. **Update Documentation**: Update system security plan if needed

---

## Agent Development Guidelines

### Agent Creation Pattern (Python)
```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from azure.identity import DefaultAzureCredential
from typing import Annotated
from pydantic import Field

# Always use managed identities or Azure CLI in dev
credential = DefaultAzureCredential()

# Create agent with typed tools
agent = ChatAgent(
    chat_client=OpenAIChatClient(credential=credential),
    name="MyAgent",
    instructions="Clear, specific instructions here",
    tools=[my_tool_function]
)

# Tool function with type annotations
def my_tool_function(
    param: Annotated[str, Field(description="Parameter description")]
) -> str:
    """Tool function docstring - visible to LLM."""
    # Implementation with input validation
    return result
```

### Agent Creation Pattern (.NET)
```csharp
using Microsoft.Agents.AI;
using Azure.Identity;
using OpenAI;

// Always use managed identities or Azure CLI in dev
var credential = new DefaultAzureCredential();
var client = new AzureOpenAIClient(
    new Uri(endpoint),
    credential
);

var agent = client
    .GetOpenAIResponseClient(deploymentName)
    .CreateAIAgent(
        name: "MyAgent",
        instructions: "Clear, specific instructions here"
    );

// Run agent
var result = await agent.RunAsync("User message");
```

### Workflow Pattern
```python
from agent_framework.workflows import Workflow, WorkflowNode

# Create workflow with explicit state management
workflow = Workflow(
    name="MyWorkflow",
    checkpoint_enabled=True,  # Always enable for federal
    state_store=redis_store
)

# Add nodes
workflow.add_node("agent1", agent1_node)
workflow.add_node("agent2", agent2_node)

# Connect nodes with data flow
workflow.add_edge("agent1", "agent2")

# Execute with observability
result = await workflow.run(
    inputs={"message": "Input"},
    trace_context=trace_context
)
```

---

## Security Standards

### Input Validation
```python
# ALWAYS validate inputs with Pydantic
from pydantic import BaseModel, Field, validator

class AgentInput(BaseModel):
    message: str = Field(..., max_length=10000)
    user_id: str = Field(..., regex=r'^[a-zA-Z0-9-]+$')

    @validator('message')
    def validate_message(cls, v):
        # Check for injection attempts
        if any(bad in v.lower() for bad in ['<script>', 'javascript:', 'onerror=']):
            raise ValueError('Potentially malicious input detected')
        return v
```

### Secrets Management
```python
# NEVER hardcode secrets
# BAD: api_key = "sk-1234567890"

# GOOD: Use Azure Key Vault
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
vault_url = "https://aurelius-kv.vault.azure.net/"
client = SecretClient(vault_url=vault_url, credential=credential)

api_key = client.get_secret("openai-api-key").value
```

### Audit Logging
```python
import logging
import structlog

# Use structured logging for audit trail
logger = structlog.get_logger()

logger.info(
    "agent_run",
    agent_id=agent.id,
    user_id=user_id,
    session_id=session_id,
    classification="CUI",
    action="run",
    result="success"
)
```

---

## Testing Requirements

### Unit Test Example
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.unit
async def test_agent_run():
    """Test agent execution with mocked LLM."""
    # Arrange
    mock_client = AsyncMock()
    mock_client.get_response.return_value = MockResponse("Test output")

    agent = ChatAgent(chat_client=mock_client, name="TestAgent")

    # Act
    result = await agent.run("Test input")

    # Assert
    assert result == "Test output"
    mock_client.get_response.assert_called_once()
```

### Integration Test Example
```python
@pytest.mark.integration
async def test_agent_with_real_llm():
    """Test agent with real Azure OpenAI (dev environment only)."""
    if os.getenv("DEPLOYMENT_ENVIRONMENT") == "production":
        pytest.skip("Integration tests disabled in production")

    agent = ChatAgent(
        chat_client=AzureOpenAIChatClient(),
        name="IntegrationTestAgent"
    )

    result = await agent.run("What is 2+2?")
    assert "4" in result.lower()
```

### Security Test Example
```python
@pytest.mark.security
async def test_agent_rejects_injection():
    """Test agent input validation against injection."""
    agent = ChatAgent(...)

    malicious_inputs = [
        "<script>alert('xss')</script>",
        "'; DROP TABLE users; --",
        "javascript:alert('xss')"
    ]

    for malicious_input in malicious_inputs:
        with pytest.raises(ValueError):
            await agent.run(malicious_input)
```

---

## Documentation Standards

### Code Documentation
```python
def process_cui_data(
    data: str,
    classification: str = "CUI"
) -> dict[str, str]:
    """
    Process Controlled Unclassified Information with proper handling.

    This function implements NIST 800-171 controls:
    - MP.2.120: CUI data protection
    - AU.3.046: Audit record generation

    Args:
        data: The CUI data to process
        classification: Data classification level (default: CUI)

    Returns:
        dict containing processed data and metadata

    Raises:
        ValueError: If data fails validation
        SecurityError: If classification requires higher controls

    Security:
        - Input validation performed
        - All access logged to audit trail
        - Data encrypted at rest and in transit

    Compliance:
        - CMMC L2 compliant
        - NIST 800-171 Rev 2 compliant

    Examples:
        >>> result = process_cui_data("Sensitive info", "CUI")
        >>> assert result['classification'] == 'CUI'
    """
    # Implementation
```

### ADR Documentation
When adding new features or making architectural changes:
1. Create ADR in `docs/decisions/`
2. Use format: `NNNN-short-title.md`
3. Include: Status, Context, Decision, Consequences, Compliance Impact

---

## Git Workflow (Project-Specific)

### Branch Naming
```
main (protected, requires 2 approvals + all gates)
├── develop (protected, requires 1 approval)
│   ├── feature/AF-{JIRA-ID}-short-description
│   ├── bugfix/AF-{JIRA-ID}-short-description
│   ├── security/CVE-YYYY-XXXXX-short-description
│   └── compliance/CMMC-{control-id}-implementation
└── release/v{MAJOR}.{MINOR}.{PATCH}
```

### Commit Message Format
```
type(scope): short description [evidence: path]

Longer description explaining:
- What changed
- Why it changed
- CMMC/NIST controls addressed (if applicable)

Evidence artifacts:
- SBOM: .aurelius/evidence/sbom/sbom-YYYYMMDD.json
- Security: .aurelius/evidence/security/scan-YYYYMMDD.json
- Tests: .aurelius/evidence/testing/coverage-YYYYMMDD.html

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Quality Gates (Enforced)

### Pre-Commit Gates (Automated by pre-commit hooks)
- ✅ Linting (Ruff, Black, isort)
- ✅ Type checking (MyPy strict, Pyright)
- ✅ Security scanning (Bandit, detect-secrets)
- ✅ Unit tests pass
- ✅ Conventional commit format

### Pre-Push Gates (CI pipeline)
- ✅ All tests pass (unit + integration)
- ✅ Coverage ≥85%
- ✅ Security scans (Bandit, Semgrep, Safety, pip-audit)
- ✅ No critical vulnerabilities
- ✅ License compliance verified

### Pre-Merge Gates (PR checks)
- ✅ All pre-push gates pass
- ✅ Mutation testing ≥65%
- ✅ Code review approved (min 2)
- ✅ Security review approved (if security changes)
- ✅ SBOM generated
- ✅ Documentation updated
- ✅ ADR created (if architectural change)

### Pre-Release Gates
- ✅ All pre-merge gates pass
- ✅ Staging deployment successful
- ✅ Performance benchmarks met
- ✅ Security authorization artifacts complete (federal)
- ✅ Release notes generated

---

## Quick Reference Commands

### Development Setup
```bash
# Clone repository
git clone https://github.com/AureliustechandTalentSolutions/Microsoft-agent-framework.git
cd Microsoft-agent-framework

# Setup Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install uv
uv pip install -e .[all]

# Setup pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Copy environment template
cp .env.example .env
# Fill in .env with actual values

# Run tests
pytest --cov --cov-report=html

# Run security scans
bandit -r . && semgrep --config=auto && safety check && pip-audit
```

### Common Tasks
```bash
# Format code
ruff check --fix . && black . && isort .

# Type check
mypy . && pyright .

# Run specific test category
pytest -m unit
pytest -m integration
pytest -m security

# Generate SBOM
cyclonedx-py -o .aurelius/evidence/sbom/sbom-$(date +%Y%m%d).json

# Check license compliance
pip-licenses --format=json --output-file=.aurelius/evidence/compliance/licenses.json

# Run mutation testing
mutmut run
mutmut results
mutmut html
```

---

## Contact & Escalation

**Technical Lead**: TBD
**Security Officer**: TBD
**Compliance Officer**: TBD

**Slack Channels**:
- #agent-framework-dev (general development)
- #agent-framework-security (security questions)
- #agent-framework-compliance (compliance questions)

**Emergency Security Contact**: security@aureliustech.com

---

## Notes

1. This project is under active development - check for updates weekly
2. All federal deployments require security authorization (ATO)
3. CUI data handling requires specific training - contact compliance team
4. When in doubt, ask in #agent-framework-dev channel

---

**Last Updated**: 2025-10-13
**Next Review**: 2025-11-13
**Owner**: Aurelius Microsoft Agent Framework Team
