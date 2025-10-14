# MLTE Integration for Microsoft Agent Framework

**Version**: 0.1.0
**Status**: Alpha
**Federal Compliance**: CMMC L2, NIST 800-171, NIST AI RMF

## Overview

This package provides seamless integration between the Microsoft Agent Framework and MLTE (Machine Learning Test and Evaluation), enabling automated, evidence-based quality assurance for AI agents with federal compliance support.

### Key Features

- **Automated Testing**: Every agent creation triggers automatic MLTE-based evaluation
- **Evidence Trail**: Complete audit trail from requirements to test results
- **Federal Compliance**: Map agent quality to NIST AI RMF and CMMC requirements
- **Multi-Agent Orchestration**: Specialized agents for each phase of evaluation
- **Seamless Integration**: Minimal changes to existing agent development workflows

## Architecture

The integration uses a multi-agent orchestration approach:

```
MLTEOrchestrator
├── NegotiationAgent (QAS generation from agent specs)
├── TestingAgent (Build and execute test suites)
├── ValidationAgent (Validate evidence and generate results)
├── ReportingAgent (Generate comprehensive reports)
└── FederalComplianceAgent (NIST AI RMF and CMMC mapping)
```

## Installation

### Basic Installation

```bash
pip install agent-framework-mlte-integration
```

### With PostgreSQL Support

```bash
pip install agent-framework-mlte-integration[rdbs]
```

### Development Installation

```bash
pip install -e .[all]
```

## Quick Start

### 1. Setup MLTE Store

```python
from mlte.session import set_context, set_store

# Development: Filesystem store
set_store("fs://./mlte-store")

# Production: PostgreSQL store
set_store("postgresql://user:pass@localhost:5432/mlte")
```

### 2. Create Agent with Evaluation

```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from agent_framework_mlte_integration import MLTEOrchestratorAgent
from agent_framework_mlte_integration.types import AgentSpec

# Create your agent
agent = ChatAgent(
    chat_client=OpenAIChatClient(),
    name="WeatherAgent",
    instructions="You are a helpful weather assistant.",
)

# Create agent specification
agent_spec = AgentSpec(
    model_id="WeatherAgent",
    version="v1.0.0",
    name="Weather Assistant Agent",
    description="Provides weather information and forecasts",
    instructions=agent.instructions,
    tools=[],
    agent_type="ChatAgent",
    metadata={"domain": "weather", "compliance": "CMMC L2"}
)

# Evaluate agent
orchestrator = MLTEOrchestratorAgent(
    chat_client=OpenAIChatClient(),
    enable_federal_compliance=True
)

evaluation_report = await orchestrator.run(agent_spec=agent_spec)
print(evaluation_report.summary)
```

### 3. View Results

```python
# Access report details
print(f"Status: {evaluation_report.status}")
print(f"Negotiation Card: {evaluation_report.negotiation_card_id}")
print(f"Test Results: {evaluation_report.test_results_id}")

# Check quality gates
if evaluation_report.gate_result:
    print(f"Passed: {len(evaluation_report.gate_result.passed)}")
    print(f"Failed: {len(evaluation_report.gate_result.failed)}")
    print(f"Deployment Allowed: {evaluation_report.gate_result.deployment_allowed}")

# Federal compliance
if evaluation_report.compliance_report:
    print(f"NIST AI RMF Characteristics: {evaluation_report.compliance_report['nist_ai_rmf']}")
    print(f"CMMC Controls: {evaluation_report.compliance_report['cmmc_controls']}")
```

## Configuration

### Environment Variables

```bash
# MLTE Configuration
MLTE_STORE_URI=postgresql://user:pass@localhost:5432/mlte
MLTE_ENABLE_EVALUATION=true
MLTE_EVALUATION_MODE=synchronous  # or: asynchronous, ci_only

# Federal Compliance
ENABLE_FEDERAL_COMPLIANCE_AGENT=true
NIST_AI_RMF_MAPPING=true
CMMC_LEVEL=2
OSCAL_EXPORT_ENABLED=true
```

### Configuration File

Create `.aurelius/mlte-config.yaml`:

```yaml
mlte:
  store:
    uri: postgresql://user:pass@localhost:5432/mlte
    type: postgresql

  evaluation:
    enabled: true
    mode: synchronous
    quality_gates:
      accuracy_min: 0.95
      security_min: 0.90
      latency_max_ms: 2000

  federal_compliance:
    enabled: true
    standards:
      - NIST AI RMF
      - CMMC L2
    oscal_export: true
```

## Components

### Orchestrator Agent

Coordinates the complete evaluation workflow:

- Receives agent creation event
- Determines evaluation requirements
- Orchestrates sub-agents in sequence
- Aggregates results and provides feedback

### Negotiation Agent

Generates Quality Attribute Scenarios (QAS) from agent specifications:

- Uses LLM to analyze agent capabilities
- Creates MLTE Negotiation Card
- Defines quality requirements

### Testing Agent

Builds and executes test suites:

- Converts QAS to TestCase objects
- Selects appropriate measurements
- Executes measurements against agent
- Collects and persists evidence

### Validation Agent

Validates evidence against requirements:

- Loads evidence and test suite
- Applies validators
- Generates TestResults
- Calculates gate pass/fail

### Reporting Agent

Generates comprehensive reports:

- Compiles MLTE Report artifact
- Creates human-readable summary
- Exports to multiple formats (JSON, HTML, PDF)

### Federal Compliance Agent

Maps results to federal standards:

- NIST AI RMF characteristic mapping
- CMMC control coverage matrix
- OSCAL document generation
- Gap analysis

## Custom Measurements

### Security Measurements

```python
from agent_framework_mlte_integration.measurements.security import (
    PromptInjectionRobustness,
    AdversarialRobustness
)
```

### Quality Measurements

```python
from agent_framework_mlte_integration.measurements.quality import (
    LLMJudgeQuality,
    ResponseAccuracy
)
```

### Performance Measurements

```python
from agent_framework_mlte_integration.measurements.performance import (
    LatencyMeasurement,
    ResourceConsumptionMeasurement
)
```

## Federal Compliance

### NIST AI RMF Mapping

Automatically maps agent evaluations to NIST AI RMF characteristics:

- Valid and Reliable
- Safe
- Secure and Resilient
- Accountable and Transparent
- Explainable and Interpretable
- Privacy Enhanced
- Fair with Harmful Bias Managed

### CMMC Level 2 Support

Provides evidence for CMMC Level 2 practices:

- Access Control (AC)
- Audit and Accountability (AU)
- Configuration Management (CM)
- Identification and Authentication (IA)
- System and Communications Protection (SC)

### OSCAL Export

Generates OSCAL-compliant documentation for federal assessments.

## CI/CD Integration

### GitHub Actions

Add to `.github/workflows/mlte-evaluation.yml`:

```yaml
name: MLTE Agent Evaluation

on:
  pull_request:
    paths:
      - 'python/packages/core/**'
      - 'python/samples/**'

jobs:
  evaluate-agents:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e python/packages/core
          pip install -e python/packages/mlte_integration

      - name: Run MLTE evaluation
        env:
          MLTE_STORE_URI: ${{ secrets.MLTE_STORE_URI }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python samples/evaluate_agents.py

      - name: Check quality gates
        run: |
          python scripts/check_mlte_gates.py || exit 1
```

## Examples

See the `samples/` directory for complete examples:

- `simple_evaluation.py` - Basic agent evaluation
- `workflow_evaluation.py` - Workflow agent evaluation
- `federal_compliance_report.py` - Generate federal compliance report

## Documentation

- [Implementation Plan](.aurelius/MLTE_IMPLEMENTATION_PLAN.md)
- [Architecture](.aurelius/MLTE_INTEGRATION_ARCHITECTURE.md)
- [Developer Guide](docs/MLTE_DEVELOPER_GUIDE.md)
- [Federal Compliance Guide](docs/MLTE_FEDERAL_COMPLIANCE_GUIDE.md)

## Contributing

This package is part of the Microsoft Agent Framework project. See the main repository for contribution guidelines.

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: https://github.com/AureliustechandTalentSolutions/Microsoft-agent-framework/issues
- Documentation: https://github.com/AureliustechandTalentSolutions/Microsoft-agent-framework/tree/main/python/packages/mlte_integration
- Contact: info@aureliustech.com

## Credits

Developed by Aurelius Tech & Talent Solutions for federal compliance and quality assurance of AI agent systems.

**SDVOSB Certified** | **MBE Certified** | **Microsoft AI Cloud Partner**
