# MLTE Integration Implementation Plan

**Version**: 1.0
**Date**: 2025-10-13
**Project**: Microsoft Agent Framework + MLTE Integration
**Organization**: Aurelius Tech & Talent Solutions

---

## Executive Summary

This document provides the detailed implementation plan for integrating MLTE (Machine Learning Test and Evaluation) into the Microsoft Agent Framework using a **multi-agent orchestration approach**. The plan leverages specialized agents to automate the implementation, testing, and deployment phases.

### Implementation Approach

**Multi-Agent Development Pattern**:
- **PLANNER Agent**: Decomposes high-level objectives into phased tasks
- **DECOMPOSER Agent**: Breaks phases into micro-tasks (5-30 min each)
- **EXECUTOR Agent**: Implements micro-tasks with evidence generation
- **REVIEWER Agent**: Validates implementation quality
- **TESTER Agent**: Expands test coverage and validates behavior
- **MERGER Agent**: Enforces all quality gates before integration

This approach ensures:
- ✅ Evidence-driven development
- ✅ Automated quality gates
- ✅ Federal compliance (CMMC L2, NIST 800-171)
- ✅ Complete audit trail
- ✅ Parallel execution where possible

---

## Phase 1: Foundation Setup (Weeks 1-2)

### 1.1 Environment Preparation

#### Tasks Breakdown

**Task 1.1.1: Install MLTE Dependencies**
- **Agent**: EXECUTOR
- **Duration**: 15 minutes
- **Acceptance Criteria**:
  - MLTE package installed: `pip install "mlte[frontend,rdbs]"`
  - Dependencies verified: `mlte --version`
  - PostgreSQL client installed (for production)
  - Test MLTE CLI: `mlte backend --help`

**Evidence Required**:
```bash
# Run and capture output
pip list | grep mlte
mlte --version
python -c "import mlte; print(mlte.__version__)"
```

**Task 1.1.2: Setup MLTE Store (Development)**
- **Agent**: EXECUTOR
- **Duration**: 20 minutes
- **Acceptance Criteria**:
  - Filesystem store directory created: `./mlte-store/`
  - Directory structure initialized
  - Test artifact save/load
  - `.gitignore` updated to exclude store data

**Implementation**:
```python
# test_mlte_store.py
from mlte.session import set_context, set_store
from mlte.negotiation.artifact import NegotiationCard

set_context("TestModel", "v0.0.1")
set_store("fs://./mlte-store")

card = NegotiationCard()
card.save(force=True, parents=True)

loaded = NegotiationCard.load(card.identifier)
assert loaded.identifier == card.identifier
print("✓ MLTE store functional")
```

**Task 1.1.3: Create Python Package Structure**
- **Agent**: EXECUTOR
- **Duration**: 30 minutes
- **Acceptance Criteria**:
  - New package: `python/packages/mlte_integration/`
  - Package structure follows Agent Framework conventions
  - `pyproject.toml` configured
  - `__init__.py` with version and exports

**Directory Structure**:
```
python/packages/mlte_integration/
├── agent_framework_mlte_integration/
│   ├── __init__.py
│   ├── orchestrator.py              # MLTEOrchestratorAgent
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── negotiation.py           # NegotiationAgent
│   │   ├── testing.py               # TestingAgent
│   │   ├── validation.py            # ValidationAgent
│   │   ├── reporting.py             # ReportingAgent
│   │   └── compliance.py            # FederalComplianceAgent
│   ├── measurements/
│   │   ├── __init__.py
│   │   ├── security.py              # Security measurements
│   │   ├── quality.py               # LLM-as-judge quality
│   │   └── performance.py           # Latency, resource metrics
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── federal.py               # NIST AI RMF, CMMC validators
│   │   └── custom.py                # Custom validators
│   ├── types.py                      # Type definitions
│   ├── config.py                     # Configuration management
│   └── utils.py                      # Utility functions
├── samples/
│   ├── simple_evaluation.py
│   ├── workflow_evaluation.py
│   └── federal_compliance_report.py
├── tests/
│   ├── test_orchestrator.py
│   ├── test_agents.py
│   ├── test_measurements.py
│   └── test_integration.py
├── pyproject.toml
└── README.md
```

**pyproject.toml**:
```toml
[project]
name = "agent-framework-mlte-integration"
version = "0.1.0"
description = "MLTE integration for Microsoft Agent Framework"
requires-python = ">=3.10"
dependencies = [
    "agent-framework-core>=0.1.0",
    "mlte>=2.2.0",
    "pydantic>=2.10.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
]
rdbs = [
    "mlte[rdbs]",
]
all = [
    "agent-framework-mlte-integration[dev,rdbs]",
]
```

---

### 1.2 Configuration Management

**Task 1.2.1: Create MLTE Configuration System**
- **Agent**: EXECUTOR
- **Duration**: 45 minutes
- **Deliverables**:
  - `config.py` with Pydantic models
  - YAML configuration file support
  - Environment variable overrides
  - Configuration validation

**Implementation**:
```python
# agent_framework_mlte_integration/config.py
from pydantic import BaseModel, Field
from typing import Dict, List, Literal
import yaml
import os

class StoreConfig(BaseModel):
    uri: str = Field(default="fs://./mlte-store")
    type: Literal["filesystem", "postgresql", "memory", "http"] = "filesystem"
    connection_pool_size: int = 10

class QualityGatesConfig(BaseModel):
    accuracy_min: float = 0.95
    security_min: float = 0.90
    latency_max_ms: int = 2000

class OrchestratorConfig(BaseModel):
    parallel_execution: bool = True
    max_workers: int = 4
    timeout_seconds: int = 300

class AgentLLMConfig(BaseModel):
    llm_model: str = "gpt-4"
    temperature: float = 0.3

class FederalComplianceConfig(BaseModel):
    enabled: bool = True
    standards: List[str] = ["NIST AI RMF", "CMMC L2"]
    oscal_export: bool = True
    audit_trail: bool = True

class MLTEConfig(BaseModel):
    store: StoreConfig = Field(default_factory=StoreConfig)
    evaluation_enabled: bool = True
    evaluation_mode: Literal["synchronous", "asynchronous", "ci_only"] = "synchronous"
    fail_on_error: bool = False
    quality_gates: QualityGatesConfig = Field(default_factory=QualityGatesConfig)
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
    agents: Dict[str, AgentLLMConfig] = Field(default_factory=dict)
    federal_compliance: FederalComplianceConfig = Field(default_factory=FederalComplianceConfig)

    @classmethod
    def load_from_yaml(cls, path: str) -> "MLTEConfig":
        """Load configuration from YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data.get("mlte", {}))

    @classmethod
    def load_from_env(cls) -> "MLTEConfig":
        """Load configuration from environment variables."""
        return cls(
            store=StoreConfig(uri=os.getenv("MLTE_STORE_URI", "fs://./mlte-store")),
            evaluation_enabled=os.getenv("MLTE_ENABLE_EVALUATION", "true").lower() == "true",
            # ... map other env vars
        )

    @classmethod
    def load(cls, config_path: str | None = None) -> "MLTEConfig":
        """Load configuration with precedence: CLI > ENV > YAML > Defaults."""
        if config_path and os.path.exists(config_path):
            config = cls.load_from_yaml(config_path)
        else:
            config = cls()

        # Override with environment variables
        env_config = cls.load_from_env()
        return config.model_copy(update=env_config.model_dump(exclude_unset=True))
```

**Task 1.2.2: Create Default Configuration Files**
- **Agent**: EXECUTOR
- **Duration**: 20 minutes
- **Deliverables**:
  - `.aurelius/mlte-config.yaml`
  - `.aurelius/mlte-config.example.yaml`
  - Environment variable template: `.env.mlte.example`

---

### 1.3 Type Definitions

**Task 1.3.1: Define Core Types**
- **Agent**: EXECUTOR
- **Duration**: 45 minutes
- **Deliverables**: `types.py` with all necessary types

**Implementation**:
```python
# agent_framework_mlte_integration/types.py
from dataclasses import dataclass
from typing import List, Dict, Any, Literal
from enum import Enum

@dataclass
class AgentSpec:
    """Specification of an agent for evaluation."""
    model_id: str
    version: str
    name: str
    description: str
    instructions: str | None
    tools: List[Dict[str, Any]]
    agent_type: str  # "ChatAgent", "WorkflowAgent", etc.
    metadata: Dict[str, Any]

@dataclass
class QualityGate:
    """Quality gate definition."""
    name: str
    test_case_id: str
    threshold: float
    comparison: Literal[">=", "<=", "==", "!=", ">", "<"]
    severity: Literal["critical", "high", "medium", "low"]
    blocking: bool

@dataclass
class GateResult:
    """Quality gate evaluation result."""
    passed: List[QualityGate]
    failed: List[QualityGate]
    blocking_failures: List[QualityGate]
    deployment_allowed: bool

class EvaluationStatus(str, Enum):
    """Status of evaluation."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class EvaluationReport:
    """Complete evaluation report."""
    agent_spec: AgentSpec
    status: EvaluationStatus
    negotiation_card_id: str | None
    test_suite_id: str | None
    test_results_id: str | None
    report_id: str | None
    gate_result: GateResult | None
    compliance_report: Dict[str, Any] | None
    summary: str
    timestamp: float

@dataclass
class ComplianceReport:
    """Federal compliance mapping report."""
    nist_ai_rmf: Dict[str, List[str]]  # Characteristic -> Test case IDs
    cmmc_controls: Dict[str, List[str]]  # Control ID -> Test case IDs
    oscal_document: Dict[str, Any] | None
    gaps: List[str]
```

---

## Phase 2: Core Agents Implementation (Weeks 3-6)

### 2.1 MLTEOrchestrator Agent

**Task 2.1.1: Implement Orchestrator Skeleton**
- **Agent**: EXECUTOR
- **Duration**: 60 minutes
- **Acceptance Criteria**:
  - `MLTEOrchestratorAgent` class inherits from `BaseAgent`
  - Initializes sub-agents
  - Implements `run()` method skeleton
  - Error handling framework

**Implementation**:
```python
# agent_framework_mlte_integration/orchestrator.py
from agent_framework import BaseAgent, AgentRunResponse, ChatClientProtocol
from agent_framework.types import ChatMessage
from mlte.session import set_context, set_store
from typing import AsyncIterator

from .agents.negotiation import NegotiationAgent
from .agents.testing import TestingAgent
from .agents.validation import ValidationAgent
from .agents.reporting import ReportingAgent
from .agents.compliance import FederalComplianceAgent
from .types import AgentSpec, EvaluationReport, EvaluationStatus
from .config import MLTEConfig

import time
import logging

logger = logging.getLogger(__name__)

class MLTEOrchestratorAgent(BaseAgent):
    """Orchestrates MLTE evaluation workflow using specialized agents."""

    def __init__(
        self,
        chat_client: ChatClientProtocol,
        config: MLTEConfig | None = None,
        enable_federal_compliance: bool = True,
    ):
        super().__init__(name="mlte_orchestrator", display_name="MLTE Orchestrator")

        self.config = config or MLTEConfig.load()
        self.chat_client = chat_client

        # Initialize sub-agents
        self.negotiation_agent = NegotiationAgent(
            chat_client=chat_client,
            config=self.config.agents.get("negotiation", {}),
        )
        self.testing_agent = TestingAgent(
            chat_client=chat_client,
            config=self.config.agents.get("testing", {}),
        )
        self.validation_agent = ValidationAgent(
            chat_client=chat_client,
            config=self.config.agents.get("validation", {}),
        )
        self.reporting_agent = ReportingAgent(
            chat_client=chat_client,
            config=self.config.agents.get("reporting", {}),
        )

        if enable_federal_compliance and self.config.federal_compliance.enabled:
            self.compliance_agent = FederalComplianceAgent(
                chat_client=chat_client,
                config=self.config.agents.get("compliance", {}),
            )
        else:
            self.compliance_agent = None

    async def run(
        self,
        messages: str | list[ChatMessage] | None = None,
        *,
        agent_spec: AgentSpec | None = None,
        **kwargs,
    ) -> AgentRunResponse:
        """Execute MLTE evaluation workflow."""
        if agent_spec is None:
            # Extract agent_spec from messages or kwargs
            agent_spec = self._extract_agent_spec(messages, kwargs)

        logger.info(f"Starting MLTE evaluation for {agent_spec.model_id}:{agent_spec.version}")

        # Initialize report
        report = EvaluationReport(
            agent_spec=agent_spec,
            status=EvaluationStatus.IN_PROGRESS,
            negotiation_card_id=None,
            test_suite_id=None,
            test_results_id=None,
            report_id=None,
            gate_result=None,
            compliance_report=None,
            summary="",
            timestamp=time.time(),
        )

        try:
            # Setup MLTE session
            set_context(agent_spec.model_id, agent_spec.version)
            set_store(self.config.store.uri)
            logger.info(f"MLTE session: {agent_spec.model_id}:{agent_spec.version}")

            # Phase 1: Negotiation
            logger.info("Phase 1: Generating Negotiation Card")
            negotiation_result = await self.negotiation_agent.run(
                agent_spec=agent_spec
            )
            report.negotiation_card_id = negotiation_result.card_id
            logger.info(f"Negotiation Card created: {negotiation_result.card_id}")

            # Phase 2: Testing
            logger.info("Phase 2: Executing Test Suite")
            testing_result = await self.testing_agent.run(
                agent_spec=agent_spec,
                negotiation_card_id=negotiation_result.card_id,
            )
            report.test_suite_id = testing_result.test_suite_id
            logger.info(f"Test Suite executed: {testing_result.test_suite_id}")

            # Phase 3: Validation
            logger.info("Phase 3: Validating Results")
            validation_result = await self.validation_agent.run(
                test_suite_id=testing_result.test_suite_id,
            )
            report.test_results_id = validation_result.test_results_id
            report.gate_result = validation_result.gate_result
            logger.info(f"Validation complete: {validation_result.summary}")

            # Phase 4: Reporting
            logger.info("Phase 4: Generating Report")
            reporting_result = await self.reporting_agent.run(
                negotiation_card_id=report.negotiation_card_id,
                test_results_id=report.test_results_id,
            )
            report.report_id = reporting_result.report_id
            logger.info(f"Report generated: {reporting_result.report_id}")

            # Phase 5: Federal Compliance (if enabled)
            if self.compliance_agent:
                logger.info("Phase 5: Federal Compliance Mapping")
                compliance_result = await self.compliance_agent.run(
                    report_id=reporting_result.report_id,
                )
                report.compliance_report = compliance_result.compliance_data
                logger.info("Compliance mapping complete")

            # Finalize report
            report.status = EvaluationStatus.COMPLETED
            report.summary = self._generate_summary(report)

            logger.info(f"MLTE evaluation completed: {report.summary}")

            return AgentRunResponse(
                messages=[
                    ChatMessage(
                        role="assistant",
                        content=self._format_report(report),
                    )
                ],
            )

        except Exception as e:
            logger.error(f"MLTE evaluation failed: {e}", exc_info=True)
            report.status = EvaluationStatus.FAILED
            report.summary = f"Evaluation failed: {str(e)}"

            if self.config.fail_on_error:
                raise

            return AgentRunResponse(
                messages=[
                    ChatMessage(
                        role="assistant",
                        content=f"⚠️ MLTE Evaluation Failed\n\n{str(e)}",
                    )
                ],
            )

    def run_stream(
        self,
        messages: str | list[ChatMessage] | None = None,
        **kwargs,
    ) -> AsyncIterator[AgentRunResponse]:
        """Streaming not supported for orchestrator."""
        raise NotImplementedError("Streaming evaluation not yet supported")

    def _extract_agent_spec(
        self, messages: str | list[ChatMessage] | None, kwargs: dict
    ) -> AgentSpec:
        """Extract AgentSpec from inputs."""
        # TODO: Implement extraction logic
        raise NotImplementedError("Agent spec extraction not yet implemented")

    def _generate_summary(self, report: EvaluationReport) -> str:
        """Generate human-readable summary."""
        if report.gate_result:
            passed = len(report.gate_result.passed)
            failed = len(report.gate_result.failed)
            status = "✅ PASSED" if report.gate_result.deployment_allowed else "❌ FAILED"
            return f"{status} - {passed} passed, {failed} failed"
        return "Evaluation incomplete"

    def _format_report(self, report: EvaluationReport) -> str:
        """Format report for display."""
        lines = [
            "# MLTE Evaluation Report",
            f"**Agent**: {report.agent_spec.name} ({report.agent_spec.model_id}:{report.agent_spec.version})",
            f"**Status**: {report.status.value}",
            f"**Summary**: {report.summary}",
            "",
            "## Artifacts",
            f"- Negotiation Card: `{report.negotiation_card_id}`",
            f"- Test Suite: `{report.test_suite_id}`",
            f"- Test Results: `{report.test_results_id}`",
            f"- Report: `{report.report_id}`",
        ]

        if report.gate_result:
            lines.extend([
                "",
                "## Quality Gates",
                f"- Passed: {len(report.gate_result.passed)}",
                f"- Failed: {len(report.gate_result.failed)}",
                f"- Deployment Allowed: {'✅ Yes' if report.gate_result.deployment_allowed else '❌ No'}",
            ])

        if report.compliance_report:
            lines.extend([
                "",
                "## Federal Compliance",
                f"- NIST AI RMF Characteristics: {len(report.compliance_report.get('nist_ai_rmf', {}))}",
                f"- CMMC Controls: {len(report.compliance_report.get('cmmc_controls', {}))}",
            ])

        return "\n".join(lines)
```

**Task 2.1.2: Add Logging and Telemetry**
- **Agent**: EXECUTOR
- **Duration**: 30 minutes
- **Acceptance Criteria**:
  - Structured logging with context
  - OpenTelemetry spans for each phase
  - Error tracking and reporting

---

### 2.2 NegotiationAgent Implementation

**Task 2.2.1: Implement QAS Generation with LLM**
- **Agent**: EXECUTOR
- **Duration**: 90 minutes
- **Acceptance Criteria**:
  - LLM-based QAS generation from agent specs
  - Structured output with validation
  - Template-based approach for common agent types
  - Manual override support

**Implementation** (see next section for full code)

**Task 2.2.2: Create QAS Templates**
- **Agent**: EXECUTOR
- **Duration**: 60 minutes
- **Deliverables**:
  - Templates for ChatAgent, WorkflowAgent
  - Domain-specific templates (customer support, data analysis, etc.)
  - Federal compliance QAS templates

---

### 2.3 TestingAgent Implementation

**Task 2.3.1: Implement Test Case Generation**
- **Agent**: EXECUTOR
- **Duration**: 90 minutes
- **Acceptance Criteria**:
  - Convert QAS to TestCase objects
  - Select appropriate measurements
  - Generate test inputs

**Task 2.3.2: Develop Custom Measurements**
- **Agent**: EXECUTOR (parallel with 2.3.1)
- **Duration**: 120 minutes
- **Deliverables**:
  - `measurements/security.py`: Prompt injection, adversarial tests
  - `measurements/quality.py`: LLM-as-judge quality evaluation
  - `measurements/performance.py`: Latency, resource consumption

---

### 2.4 ValidationAgent Implementation

**Task 2.4.1: Implement Validation Logic**
- **Agent**: EXECUTOR
- **Duration**: 60 minutes
- **Acceptance Criteria**:
  - Load evidence and test suite
  - Execute validators
  - Generate TestResults
  - Calculate gate pass/fail

**Task 2.4.2: Add LLM-Based Remediation Suggestions**
- **Agent**: EXECUTOR
- **Duration**: 45 minutes
- **Acceptance Criteria**:
  - Analyze failed tests
  - Generate remediation suggestions using LLM
  - Include code examples where applicable

---

### 2.5 ReportingAgent Implementation

**Task 2.5.1: Implement Report Generation**
- **Agent**: EXECUTOR
- **Duration**: 60 minutes
- **Acceptance Criteria**:
  - Compile MLTE Report artifact
  - Generate human-readable summary
  - Export to multiple formats (JSON, HTML, PDF)

**Task 2.5.2: Add Visualization**
- **Agent**: EXECUTOR
- **Duration**: 90 minutes
- **Deliverables**:
  - Charts for metric trends
  - Quality gate status visualization
  - Comparative analysis across versions

---

### 2.6 FederalComplianceAgent Implementation

**Task 2.6.1: Implement NIST AI RMF Mapping**
- **Agent**: EXECUTOR
- **Duration**: 120 minutes
- **Acceptance Criteria**:
  - Map QAS to NIST AI RMF characteristics
  - Generate coverage report
  - Identify gaps

**Task 2.6.2: Implement CMMC Mapping**
- **Agent**: EXECUTOR (parallel with 2.6.1)
- **Duration**: 120 minutes
- **Acceptance Criteria**:
  - Map tests to CMMC L2 practices
  - Generate control coverage matrix
  - Evidence linkage

**Task 2.6.3: Implement OSCAL Export**
- **Agent**: EXECUTOR
- **Duration**: 90 minutes
- **Acceptance Criteria**:
  - Generate OSCAL-compliant JSON
  - Include all evidence references
  - Validate against OSCAL schema

---

## Phase 3: Integration and Automation (Weeks 7-10)

### 3.1 Agent Framework Integration

**Task 3.1.1: Implement Middleware Hook**
- **Agent**: EXECUTOR
- **Duration**: 60 minutes
- **Deliverables**: `MLTEEvaluationMiddleware` class

**Task 3.1.2: Implement Context Provider Hook**
- **Agent**: EXECUTOR (parallel with 3.1.1)
- **Duration**: 60 minutes
- **Deliverables**: `MLTEContextProvider` class

**Task 3.1.3: DevUI Integration**
- **Agent**: EXECUTOR
- **Duration**: 90 minutes
- **Acceptance Criteria**:
  - Add MLTE button to DevUI
  - Display evaluation status
  - Show reports in UI

---

### 3.2 Workspace Configuration

**Task 3.2.1: Add MLTE Tasks to VS Code**
- **Agent**: EXECUTOR
- **Duration**: 45 minutes
- **Deliverables**: Update `.vscode/tasks.json`

**Tasks to Add**:
```json
{
  "label": "MLTE: Start Backend (Development)",
  "type": "shell",
  "command": "mlte backend --host 127.0.0.1 --port 8080 --store-uri fs://./mlte-store",
  "isBackground": true,
  "problemMatcher": {
    "background": {
      "beginsPattern": ".*Starting.*",
      "endsPattern": ".*Application startup complete.*"
    }
  }
},
{
  "label": "MLTE: Start Frontend",
  "type": "shell",
  "command": "mlte ui --host 127.0.0.1 --port 8000",
  "isBackground": true
},
{
  "label": "MLTE: Evaluate Sample Agent",
  "type": "shell",
  "command": "python samples/mlte/evaluate_agent.py"
},
{
  "label": "MLTE: Run Tests",
  "type": "shell",
  "command": "pytest python/packages/mlte_integration/tests/ -v"
}
```

**Task 3.2.2: Add MLTE Debug Configurations**
- **Agent**: EXECUTOR
- **Duration**: 30 minutes
- **Deliverables**: Update `.vscode/launch.json`

**Task 3.2.3: Update Workspace Documentation**
- **Agent**: EXECUTOR
- **Duration**: 45 minutes
- **Deliverables**:
  - Update `WORKSPACE_GUIDE.md`
  - Update `QUICK_REFERENCE.md`
  - Create `MLTE_DEVELOPER_GUIDE.md`

---

### 3.3 CI/CD Integration

**Task 3.3.1: Create GitHub Actions Workflow**
- **Agent**: EXECUTOR
- **Duration**: 90 minutes
- **Deliverables**: `.github/workflows/mlte-evaluation.yml`

**Workflow**:
```yaml
name: MLTE Agent Evaluation

on:
  pull_request:
    paths:
      - 'python/packages/core/**'
      - 'python/samples/**'
  push:
    branches: [main]

jobs:
  evaluate-agents:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: mlte
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Agent Framework
        run: |
          pip install -e python/packages/core
          pip install -e python/packages/mlte_integration

      - name: Install MLTE
        run: pip install "mlte[rdbs]"

      - name: Setup MLTE Database
        run: |
          python -c "from mlte.backend.core import store_adapter; store_adapter.create_tables('postgresql://postgres:postgres@localhost:5432/mlte')"

      - name: Discover Sample Agents
        id: discover
        run: |
          python .aurelius/scripts/discover_agents.py > agents.json
          echo "agents=$(cat agents.json)" >> $GITHUB_OUTPUT

      - name: Evaluate Agents
        env:
          MLTE_STORE_URI: postgresql://postgres:postgres@localhost:5432/mlte
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
          AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
        run: |
          python .aurelius/scripts/run_mlte_evaluation.py --agents agents.json

      - name: Check Quality Gates
        run: |
          python .aurelius/scripts/check_mlte_gates.py || exit 1

      - name: Generate Report Summary
        run: |
          python .aurelius/scripts/generate_report_summary.py > $GITHUB_STEP_SUMMARY

      - name: Upload MLTE Reports
        uses: actions/upload-artifact@v3
        with:
          name: mlte-reports-${{ github.sha }}
          path: mlte-reports/

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('mlte-reports/summary.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## MLTE Evaluation Results\n\n${summary}`
            });
```

**Task 3.3.2: Create Pre-commit Hook**
- **Agent**: EXECUTOR
- **Duration**: 30 minutes
- **Deliverables**: Add to `.pre-commit-config.yaml`

**Task 3.3.3: Add Quality Gate Enforcement**
- **Agent**: EXECUTOR
- **Duration**: 45 minutes
- **Deliverables**: Script to fail CI if gates not met

---

## Phase 4: Testing and Validation (Weeks 11-14)

### 4.1 Unit Tests

**Task 4.1.1-4.1.10: Write Unit Tests** (Parallel execution)
- **Agent**: TESTER (specialized agent)
- **Duration**: 30 minutes each
- **Coverage Target**: 85%

Tests needed:
1. `test_orchestrator.py`: Orchestrator logic
2. `test_negotiation_agent.py`: QAS generation
3. `test_testing_agent.py`: Test case generation
4. `test_validation_agent.py`: Validation logic
5. `test_reporting_agent.py`: Report generation
6. `test_compliance_agent.py`: Compliance mapping
7. `test_measurements.py`: Custom measurements
8. `test_validators.py`: Custom validators
9. `test_config.py`: Configuration management
10. `test_types.py`: Type validation

---

### 4.2 Integration Tests

**Task 4.2.1: End-to-End Evaluation Test**
- **Agent**: TESTER
- **Duration**: 60 minutes
- **Acceptance Criteria**:
  - Create sample agent
  - Run complete MLTE evaluation
  - Verify all artifacts created
  - Check quality gates

**Task 4.2.2: DevUI Integration Test**
- **Agent**: TESTER (parallel with 4.2.1)
- **Duration**: 60 minutes
- **Acceptance Criteria**:
  - Start DevUI with MLTE enabled
  - Trigger evaluation from UI
  - Verify report display

**Task 4.2.3: CI/CD Pipeline Test**
- **Agent**: TESTER (parallel with 4.2.1, 4.2.2)
- **Duration**: 45 minutes
- **Acceptance Criteria**:
  - Trigger GitHub Actions workflow
  - Verify all steps pass
  - Check artifact uploads

---

### 4.3 Sample Implementations

**Task 4.3.1-4.3.3: Create Sample Agents with Evaluation** (Parallel)
- **Agent**: EXECUTOR
- **Duration**: 60 minutes each

Samples:
1. Simple ChatAgent evaluation
2. Workflow evaluation
3. Federal compliance report generation

---

## Phase 5: Documentation and Training (Weeks 15-16)

### 5.1 Documentation

**Task 5.1.1: Create MLTE Developer Guide**
- **Agent**: EXECUTOR
- **Duration**: 120 minutes
- **Deliverables**: `MLTE_DEVELOPER_GUIDE.md`

**Task 5.1.2: Create Federal Compliance Guide**
- **Agent**: EXECUTOR (parallel with 5.1.1)
- **Duration**: 90 minutes
- **Deliverables**: `MLTE_FEDERAL_COMPLIANCE_GUIDE.md`

**Task 5.1.3: Update Package README**
- **Agent**: EXECUTOR (parallel with 5.1.1, 5.1.2)
- **Duration**: 45 minutes
- **Deliverables**: Comprehensive README for mlte_integration package

**Task 5.1.4: Create Quick Start Tutorial**
- **Agent**: EXECUTOR
- **Duration**: 60 minutes
- **Deliverables**: `MLTE_QUICKSTART.md` + Jupyter notebook

---

### 5.2 Training Materials

**Task 5.2.1: Create Video Tutorial**
- **Agent**: Human (with AI assistance)
- **Duration**: 240 minutes
- **Deliverables**: 15-minute walkthrough video

**Task 5.2.2: Create Presentation Deck**
- **Agent**: EXECUTOR
- **Duration**: 90 minutes
- **Deliverables**: PowerPoint/PDF for team training

---

## Phase 6: Production Deployment (Weeks 17-20)

### 6.1 Production Environment Setup

**Task 6.1.1: Provision Azure Resources**
- **Agent**: EXECUTOR
- **Duration**: 120 minutes
- **Deliverables**:
  - Azure PostgreSQL database
  - Azure Kubernetes Service (AKS) cluster
  - Azure Key Vault for secrets
  - Azure Blob Storage for catalogs

**Task 6.1.2: Create Docker Images**
- **Agent**: EXECUTOR (parallel with 6.1.1)
- **Duration**: 90 minutes
- **Deliverables**:
  - `Dockerfile` for MLTE backend
  - `Dockerfile` for MLTE frontend
  - `Dockerfile` for evaluation agents

**Task 6.1.3: Create Kubernetes Manifests**
- **Agent**: EXECUTOR (parallel with 6.1.1, 6.1.2)
- **Duration**: 120 minutes
- **Deliverables**:
  - Deployments, Services, Ingress
  - ConfigMaps and Secrets
  - Persistent Volume Claims

---

### 6.2 Security Hardening

**Task 6.2.1: Security Audit**
- **Agent**: REVIEWER (specialized security focus)
- **Duration**: 180 minutes
- **Deliverables**: Security audit report

**Task 6.2.2: Penetration Testing**
- **Agent**: Human security expert
- **Duration**: 480 minutes
- **Deliverables**: Pen test report + remediation plan

**Task 6.2.3: Implement Remediations**
- **Agent**: EXECUTOR
- **Duration**: Variable (based on findings)

---

### 6.3 Performance Optimization

**Task 6.3.1: Load Testing**
- **Agent**: TESTER
- **Duration**: 120 minutes
- **Deliverables**: Load test report

**Task 6.3.2: Optimize Bottlenecks**
- **Agent**: EXECUTOR
- **Duration**: Variable
- **Deliverables**: Performance improvement report

---

### 6.4 Go-Live

**Task 6.4.1: Staged Rollout**
- **Agent**: Human (deployment lead)
- **Duration**: 120 minutes
- **Deliverables**: Production deployment

**Task 6.4.2: Monitoring Setup**
- **Agent**: EXECUTOR (parallel with 6.4.1)
- **Duration**: 90 minutes
- **Deliverables**:
  - Azure Monitor dashboards
  - Alerts and notifications
  - Log aggregation

**Task 6.4.3: Create Runbook**
- **Agent**: EXECUTOR
- **Duration**: 120 minutes
- **Deliverables**: Operations runbook for on-call team

---

## Multi-Agent Orchestration Strategy

### Parallel Execution Opportunities

**Week 3-4 (Phase 2.1-2.2)**:
```yaml
parallel_agents:
  - executor_1: Orchestrator implementation
  - executor_2: NegotiationAgent implementation
  - executor_3: Configuration system
  - executor_4: Type definitions
max_parallelism: 4
```

**Week 5-6 (Phase 2.3-2.6)**:
```yaml
parallel_agents:
  - executor_1: TestingAgent
  - executor_2: ValidationAgent
  - executor_3: ReportingAgent
  - executor_4: ComplianceAgent
  - tester_1: Unit tests for negotiation
  - tester_2: Unit tests for config
max_parallelism: 6
```

**Week 11-12 (Phase 4)**:
```yaml
parallel_agents:
  - tester_1: Unit tests group A (tests 1-3)
  - tester_2: Unit tests group B (tests 4-6)
  - tester_3: Unit tests group C (tests 7-10)
  - tester_4: Integration tests
  - executor_1: Sample implementations
max_parallelism: 5
```

---

## Evidence Requirements

### Per Task Evidence

Each task must generate:
1. **Code Diffs**: Unified diff patches
2. **Test Results**: pytest output with coverage
3. **Static Analysis**: Ruff, MyPy, Bandit reports
4. **Documentation**: Updated docs with changes
5. **Commit Hash**: Git commit reference

### Phase-Level Evidence

Each phase must produce:
1. **Phase Report**: Summary of all tasks
2. **Quality Metrics**: Coverage, mutation scores
3. **Security Scan**: Bandit + Safety reports
4. **SBOM**: CycloneDX JSON
5. **Licenses**: pip-licenses JSON

---

## Risk Mitigation

### Technical Risks

| Risk | Mitigation |
|------|-----------|
| LLM API failures | Retry logic + fallback models |
| MLTE store corruption | Backup/restore procedures + validation |
| Performance degradation | Async evaluation + caching |
| Integration bugs | Comprehensive testing + canary deployments |

### Schedule Risks

| Risk | Mitigation |
|------|-----------|
| Scope creep | Strict phase boundaries + change control |
| Resource availability | Cross-training + buffer time |
| External dependencies | Early identification + alternatives |
| Federal validation delays | Parallel track + early engagement |

---

## Success Criteria

### Phase Completion Gates

Each phase must meet:
- [ ] All tasks completed with evidence
- [ ] Unit tests: ≥85% coverage
- [ ] Mutation tests: ≥65% score
- [ ] Security scans: 0 critical issues
- [ ] Type checking: 0 errors
- [ ] Documentation: All new code documented
- [ ] Peer review: Approved by 2+ reviewers

### Final Acceptance Criteria

- [ ] Complete agent creation → evaluation flow functional
- [ ] All 5 specialized agents implemented and tested
- [ ] Federal compliance mapping accurate (validated by expert)
- [ ] CI/CD pipeline operational
- [ ] Production environment deployed
- [ ] Security audit passed
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Training delivered

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Phase 1: Foundation** | 2 weeks | Package structure, config, types |
| **Phase 2: Core Agents** | 4 weeks | 5 specialized agents implemented |
| **Phase 3: Integration** | 4 weeks | Hooks, workspace config, CI/CD |
| **Phase 4: Testing** | 4 weeks | Unit tests, integration tests, samples |
| **Phase 5: Documentation** | 2 weeks | Guides, tutorials, training |
| **Phase 6: Production** | 4 weeks | Deployment, security, go-live |
| **Total** | **20 weeks** | Complete MLTE integration |

---

## Next Steps

1. **Review and Approve Plan**: Stakeholder sign-off
2. **Assign Agents**: Map tasks to specific agent instances
3. **Setup Project Tracking**: Jira/GitHub Projects for task tracking
4. **Kickoff Meeting**: Align team on approach
5. **Begin Phase 1**: Start with foundation setup

---

**Plan Version**: 1.0
**Last Updated**: 2025-10-13
**Owner**: Aurelius Tech & Talent Solutions
**Status**: Ready for Review

---

*This implementation plan will be updated weekly based on progress and lessons learned.*
