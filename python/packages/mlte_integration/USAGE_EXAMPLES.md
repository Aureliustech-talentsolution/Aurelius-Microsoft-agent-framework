# MLTE Integration Usage Examples

## Configuration Management

### Basic Configuration

```python
from agent_framework_mlte_integration.config import MLTEConfig

# Load with defaults
config = MLTEConfig.load()

# Access configuration
print(f"Store URI: {config.store.uri}")
print(f"Evaluation enabled: {config.evaluation_enabled}")
print(f"Quality gates: {config.quality_gates.accuracy_min}")
```

### Load from YAML File

```python
# Load from specific file
config = MLTEConfig.load(".aurelius/mlte-config.yaml")

# Or load directly from YAML
config = MLTEConfig.load_from_yaml(".aurelius/mlte-config.yaml")
```

### Load from Environment Variables

```python
import os

# Set environment variables
os.environ["MLTE_STORE_URI"] = "postgresql://localhost:5432/mlte"
os.environ["MLTE_ENABLE_EVALUATION"] = "true"
os.environ["MLTE_EVALUATION_MODE"] = "asynchronous"

# Load from environment
config = MLTEConfig.load_from_env()
```

### Configuration Precedence

The `load()` method uses hierarchical precedence: ENV > YAML > Defaults

```python
# This will apply:
# 1. Defaults
# 2. YAML file values (if provided)
# 3. Environment variable overrides
config = MLTEConfig.load(".aurelius/mlte-config.yaml")
```

### Export Configuration

```python
# Create configuration
config = MLTEConfig(
    evaluation_mode="asynchronous",
    store=StoreConfig(uri="postgresql://localhost/mlte"),
    quality_gates=QualityGatesConfig(accuracy_min=0.92)
)

# Export to YAML
config.to_yaml("my-config.yaml")
```

### Federal Compliance Validation

```python
# Validate configuration meets federal requirements
config = MLTEConfig.load()
errors = config.validate_federal_requirements()

if errors:
    print("Configuration errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Configuration is compliant")
```

## Type Usage

### Creating Agent Specifications

```python
from agent_framework_mlte_integration.types import AgentSpec

# Create agent spec for evaluation
agent_spec = AgentSpec(
    model_id="weather_agent",
    version="1.0.0",
    name="Weather Assistant",
    description="Provides weather information and forecasts",
    instructions="You are a helpful weather assistant...",
    tools=[
        {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {"location": "string"}
        }
    ],
    agent_type="ChatAgent",
    metadata={
        "environment": "production",
        "team": "weather-team"
    }
)

# Validate (raises ValueError if invalid)
# AgentSpec automatically validates required fields
```

### Defining Quality Gates

```python
from agent_framework_mlte_integration.types import QualityGate

# Define quality gates for agent evaluation
accuracy_gate = QualityGate(
    name="Minimum Accuracy",
    test_case_id="accuracy",
    threshold=0.95,
    comparison=">=",
    severity="critical",
    blocking=True,
    description="Agent must achieve 95% accuracy"
)

latency_gate = QualityGate(
    name="Maximum Latency",
    test_case_id="latency",
    threshold=2000,  # milliseconds
    comparison="<=",
    severity="high",
    blocking=False,
    description="Agent should respond within 2 seconds"
)

# Evaluate gate
accuracy_value = 0.96
if accuracy_gate.evaluate(accuracy_value):
    print("✓ Accuracy gate passed")
else:
    print("✗ Accuracy gate failed")
```

### Working with Gate Results

```python
from agent_framework_mlte_integration.types import GateResult

# Create gate result
result = GateResult(
    passed=[accuracy_gate],
    failed=[latency_gate],
    blocking_failures=[],
    deployment_allowed=True
)

# Analyze results
print(f"Pass rate: {result.pass_rate:.1%}")
print(f"Summary: {result.summary}")
print(f"Deployment allowed: {result.deployment_allowed}")

# Check specific failures
if result.blocking_failures:
    print("Blocking failures:")
    for gate in result.blocking_failures:
        print(f"  - {gate.name}: {gate.description}")
```

### Creating Evaluation Reports

```python
from agent_framework_mlte_integration.types import (
    EvaluationReport,
    EvaluationStatus,
    GateResult
)

# Create evaluation report
report = EvaluationReport(
    agent_spec=agent_spec,
    status=EvaluationStatus.COMPLETED,
    negotiation_card_id="card-12345",
    test_suite_id="suite-67890",
    test_results_id="results-abcde",
    report_id="report-fghij",
    gate_result=result,
    summary="Evaluation completed successfully",
    duration_seconds=125.5
)

# Check report status
if report.is_complete and report.is_passed:
    print("✓ Agent passed evaluation")
else:
    print("✗ Agent failed evaluation")

# Export to dictionary
report_dict = report.to_dict()
print(f"Agent: {report_dict['agent']['name']}")
print(f"Status: {report_dict['status']}")
print(f"Duration: {report_dict['duration_seconds']}s")
```

### Federal Compliance Reporting

```python
from agent_framework_mlte_integration.types import ComplianceReport

# Create compliance report
compliance = ComplianceReport(
    nist_ai_rmf={
        "Valid and Reliable": ["accuracy", "precision_recall"],
        "Safe": ["robustness", "error_handling"],
        "Secure and Resilient": ["prompt_injection", "input_validation"],
        "Accountable and Transparent": ["explainability"],
    },
    cmmc_controls={
        "AC.L2-3.1.1": ["access_control_test"],
        "IA.L2-3.5.1": ["authentication_test"],
        "AU.L2-3.3.1": ["audit_logging_test"],
    },
    nist_800_171={
        "3.1.1": ["access_control_test"],
        "3.3.1": ["audit_logging_test"],
    },
    gaps=["Privacy Enhanced characteristic needs more coverage"],
    recommendations=[
        "Add PII detection tests",
        "Implement data anonymization validation"
    ]
)

# Analyze coverage
print(f"NIST AI RMF Coverage: {compliance.nist_ai_rmf_coverage:.1%}")
print(f"CMMC Coverage: {compliance.cmmc_coverage:.1%}")

# Export compliance data
compliance_dict = compliance.to_dict()
print(f"Total gaps: {len(compliance_dict['gaps'])}")
print(f"Recommendations: {len(compliance_dict['recommendations'])}")
```

### Test Inputs and Measurements

```python
from agent_framework_mlte_integration.types import TestInput, MeasurementResult

# Define test input
test_input = TestInput(
    test_case_id="accuracy-001",
    input_data={
        "query": "What's the weather in Seattle?",
        "context": "production"
    },
    expected_output="Current weather in Seattle: Partly cloudy, 65°F",
    metadata={"test_set": "weather_queries"}
)

# Record measurement result
measurement = MeasurementResult(
    test_case_id="accuracy-001",
    measurement_type="accuracy",
    value=0.96,
    unit="percentage",
    passed=True,
    metadata={
        "model": "gpt-4",
        "execution_time_ms": 1250
    }
)

print(f"Test {measurement.test_case_id}: {measurement.value} {measurement.unit}")
print(f"Passed: {measurement.passed}")
```

### Quality Attribute Scenarios (QAS)

```python
from agent_framework_mlte_integration.types import QASDescriptor

# Define QAS for negotiation
qas = QASDescriptor(
    quality="accuracy",
    stimulus="User asks a factual weather question",
    source="User input via chat interface",
    environment="Production with high load",
    response="Agent provides accurate weather data within 2 seconds",
    measure="Accuracy >= 95%, Latency <= 2000ms",
    metadata={
        "priority": "high",
        "category": "functional"
    }
)

print(f"Quality attribute: {qas.quality}")
print(f"Measure: {qas.measure}")
```

## Complete Example: Agent Evaluation Workflow

```python
from agent_framework_mlte_integration.config import MLTEConfig
from agent_framework_mlte_integration.types import (
    AgentSpec,
    QualityGate,
    EvaluationReport,
    EvaluationStatus
)

# 1. Load configuration
config = MLTEConfig.load(".aurelius/mlte-config.yaml")

# 2. Validate federal requirements
errors = config.validate_federal_requirements()
if errors:
    print("Configuration errors detected!")
    for error in errors:
        print(f"  - {error}")
    exit(1)

# 3. Define agent specification
agent_spec = AgentSpec(
    model_id="customer_support_agent",
    version="2.1.0",
    name="Customer Support Assistant",
    description="Handles customer inquiries and support tickets",
    instructions="You are a professional customer support agent...",
    tools=[
        {"name": "search_kb", "description": "Search knowledge base"},
        {"name": "create_ticket", "description": "Create support ticket"},
    ],
    agent_type="ChatAgent",
    metadata={"department": "support", "classification": "CUI"}
)

# 4. Define quality gates
quality_gates = [
    QualityGate(
        name="Minimum Accuracy",
        test_case_id="accuracy",
        threshold=config.quality_gates.accuracy_min,
        comparison=">=",
        severity="critical",
        blocking=True
    ),
    QualityGate(
        name="Security Threshold",
        test_case_id="security",
        threshold=config.quality_gates.security_min,
        comparison=">=",
        severity="critical",
        blocking=True
    ),
    QualityGate(
        name="Maximum Latency",
        test_case_id="latency",
        threshold=config.quality_gates.latency_max_ms,
        comparison="<=",
        severity="high",
        blocking=False
    ),
]

# 5. Run evaluation (simulated)
# In practice, this would be done by MLTEOrchestratorAgent
print(f"Evaluating agent: {agent_spec.name} v{agent_spec.version}")
print(f"Store: {config.store.uri}")
print(f"Quality gates: {len(quality_gates)}")
print(f"Federal compliance: {config.federal_compliance.enabled}")

# 6. Process results
# (Results would come from actual MLTE evaluation)
print("\nEvaluation complete!")
```

## Testing Examples

### Testing Type Validation

```python
import pytest
from agent_framework_mlte_integration.types import AgentSpec

def test_agent_spec_validation():
    """Test that AgentSpec validates required fields."""
    # Valid spec
    spec = AgentSpec(
        model_id="test",
        version="1.0.0",
        name="Test Agent",
        description="Test description"
    )
    assert spec.model_id == "test"

    # Invalid spec (missing model_id)
    with pytest.raises(ValueError):
        AgentSpec(
            model_id="",
            version="1.0.0",
            name="Test",
            description="Test"
        )
```

### Testing Configuration Loading

```python
import tempfile
import yaml
from pathlib import Path
from agent_framework_mlte_integration.config import MLTEConfig

def test_config_loading():
    """Test configuration loading from YAML."""
    # Create temporary config file
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test-config.yaml"

        config_data = {
            "mlte": {
                "store": {"uri": "fs://./test-store"},
                "evaluation_enabled": True,
                "evaluation_mode": "synchronous"
            }
        }

        with open(config_path, "w") as f:
            yaml.dump(config_data, f)

        # Load configuration
        config = MLTEConfig.load_from_yaml(str(config_path))

        assert config.store.uri == "fs://./test-store"
        assert config.evaluation_enabled is True
```

## Factory Methods

### Create Default Production Configuration

```python
from agent_framework_mlte_integration.config import (
    MLTEConfig,
    StoreConfig,
    QualityGatesConfig,
    FederalComplianceConfig
)

def create_production_config(postgres_uri: str) -> MLTEConfig:
    """Create production-ready MLTE configuration."""
    return MLTEConfig(
        store=StoreConfig(
            uri=postgres_uri,
            type="postgresql",
            connection_pool_size=20
        ),
        evaluation_enabled=True,
        evaluation_mode="asynchronous",
        fail_on_error=False,  # Don't fail prod builds
        quality_gates=QualityGatesConfig(
            accuracy_min=0.95,
            security_min=0.90,
            latency_max_ms=2000,
            memory_max_mb=512
        ),
        federal_compliance=FederalComplianceConfig(
            enabled=True,
            standards=["NIST AI RMF", "CMMC L2", "NIST 800-171"],
            oscal_export=True,
            audit_trail=True,
            classification="CUI"
        )
    )

# Usage
prod_config = create_production_config("postgresql://prod-host:5432/mlte")
```

### Create Development Configuration

```python
def create_dev_config() -> MLTEConfig:
    """Create development MLTE configuration."""
    return MLTEConfig(
        store=StoreConfig(uri="fs://./dev-mlte-store"),
        evaluation_enabled=True,
        evaluation_mode="synchronous",
        fail_on_error=False,
        quality_gates=QualityGatesConfig(
            accuracy_min=0.80,  # Lower for dev
            security_min=0.80,
            latency_max_ms=5000,  # More relaxed
            memory_max_mb=1024
        ),
        federal_compliance=FederalComplianceConfig(
            enabled=False  # Optional in dev
        )
    )

# Usage
dev_config = create_dev_config()
```

### Create CI/CD Configuration

```python
def create_ci_config(postgres_uri: str) -> MLTEConfig:
    """Create CI/CD MLTE configuration."""
    return MLTEConfig(
        store=StoreConfig(
            uri=postgres_uri,
            type="postgresql",
            connection_pool_size=10
        ),
        evaluation_enabled=True,
        evaluation_mode="ci_only",
        fail_on_error=True,  # Fail CI on errors
        quality_gates=QualityGatesConfig(
            accuracy_min=0.95,
            security_min=0.90,
            latency_max_ms=2000,
            memory_max_mb=512
        ),
        federal_compliance=FederalComplianceConfig(
            enabled=True,
            audit_trail=True,
            oscal_export=True
        )
    )

# Usage
ci_config = create_ci_config("postgresql://ci-host:5432/mlte_ci")
```

## Best Practices

### 1. Always Validate Federal Requirements

```python
config = MLTEConfig.load()
errors = config.validate_federal_requirements()
if errors and config.federal_compliance.enabled:
    raise ValueError(f"Federal compliance errors: {errors}")
```

### 2. Use Environment Variables for Secrets

```python
# Never hardcode credentials in config files
# Use environment variables instead
os.environ["MLTE_STORE_URI"] = "postgresql://user:${DB_PASSWORD}@host/mlte"
config = MLTEConfig.load_from_env()
```

### 3. Separate Configs for Different Environments

```yaml
# dev-config.yaml
mlte:
  store:
    uri: "fs://./dev-store"
  evaluation_mode: synchronous

# prod-config.yaml
mlte:
  store:
    uri: "postgresql://prod-host/mlte"
  evaluation_mode: asynchronous
```

### 4. Version Your Configuration Files

```python
# Include version in config for tracking
config.metadata = {
    "config_version": "1.0.0",
    "last_updated": "2025-10-13",
    "environment": "production"
}
```

### 5. Test Configuration Before Deployment

```python
def validate_config(config: MLTEConfig) -> None:
    """Validate configuration before deployment."""
    # Check federal requirements
    errors = config.validate_federal_requirements()
    assert not errors, f"Config errors: {errors}"

    # Test store connection (if possible)
    # ...

    # Verify quality gates are reasonable
    assert 0.0 <= config.quality_gates.accuracy_min <= 1.0
    assert config.quality_gates.latency_max_ms > 0
```

## Federal Compliance Notes

When working with federal projects:

1. **Always enable federal compliance**:
   ```python
   config.federal_compliance.enabled = True
   ```

2. **Enable audit trail**:
   ```python
   config.federal_compliance.audit_trail = True
   ```

3. **Use PostgreSQL store (not memory)**:
   ```python
   config.store.type = "postgresql"
   ```

4. **Set appropriate classification**:
   ```python
   config.federal_compliance.classification = "CUI"
   ```

5. **Meet CMMC L2 security thresholds**:
   ```python
   config.quality_gates.security_min >= 0.90
   ```
