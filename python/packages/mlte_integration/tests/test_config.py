"""
Unit tests for MLTE integration configuration management.

Tests validate configuration loading from YAML files, environment variables,
and hierarchical precedence. Tests ensure federal compliance requirements.

Federal Compliance: Configuration management per CM-6.
"""

import os
from pathlib import Path

import pytest
import yaml

from agent_framework_mlte_integration.config import (
    MLTEConfig,
    StoreConfig,
    QualityGatesConfig,
    OrchestratorConfig,
    AgentLLMConfig,
    FederalComplianceConfig,
)


class TestStoreConfig:
    """Tests for StoreConfig model."""

    def test_store_config_defaults(self):
        """Test StoreConfig default values."""
        config = StoreConfig()
        assert config.uri == "fs://./mlte-store"
        assert config.type == "filesystem"
        assert config.connection_pool_size == 10

    def test_store_config_custom_values(self):
        """Test StoreConfig with custom values."""
        config = StoreConfig(
            uri="postgresql://localhost:5432/mlte",
            type="postgresql",
            connection_pool_size=20,
        )
        assert config.uri == "postgresql://localhost:5432/mlte"
        assert config.type == "postgresql"
        assert config.connection_pool_size == 20

    def test_store_config_validation(self):
        """Test StoreConfig validation."""
        # Valid pool sizes
        StoreConfig(connection_pool_size=1)
        StoreConfig(connection_pool_size=100)

        # Invalid pool sizes
        with pytest.raises(ValueError):
            StoreConfig(connection_pool_size=0)

        with pytest.raises(ValueError):
            StoreConfig(connection_pool_size=101)


class TestQualityGatesConfig:
    """Tests for QualityGatesConfig model."""

    def test_quality_gates_config_defaults(self):
        """Test QualityGatesConfig default values."""
        config = QualityGatesConfig()
        assert config.accuracy_min == 0.95
        assert config.security_min == 0.90
        assert config.latency_max_ms == 2000
        assert config.memory_max_mb == 512

    def test_quality_gates_config_custom_values(self):
        """Test QualityGatesConfig with custom values."""
        config = QualityGatesConfig(
            accuracy_min=0.90,
            security_min=0.85,
            latency_max_ms=3000,
            memory_max_mb=1024,
        )
        assert config.accuracy_min == 0.90
        assert config.security_min == 0.85
        assert config.latency_max_ms == 3000
        assert config.memory_max_mb == 1024

    def test_quality_gates_config_validation(self):
        """Test QualityGatesConfig validation."""
        # Valid accuracy range
        QualityGatesConfig(accuracy_min=0.0)
        QualityGatesConfig(accuracy_min=1.0)

        # Invalid accuracy values
        with pytest.raises(ValueError):
            QualityGatesConfig(accuracy_min=-0.1)

        with pytest.raises(ValueError):
            QualityGatesConfig(accuracy_min=1.1)

        # Valid latency
        QualityGatesConfig(latency_max_ms=1)

        # Invalid latency
        with pytest.raises(ValueError):
            QualityGatesConfig(latency_max_ms=0)


class TestOrchestratorConfig:
    """Tests for OrchestratorConfig model."""

    def test_orchestrator_config_defaults(self):
        """Test OrchestratorConfig default values."""
        config = OrchestratorConfig()
        assert config.parallel_execution is True
        assert config.max_workers == 4
        assert config.timeout_seconds == 300

    def test_orchestrator_config_custom_values(self):
        """Test OrchestratorConfig with custom values."""
        config = OrchestratorConfig(
            parallel_execution=False, max_workers=8, timeout_seconds=600
        )
        assert config.parallel_execution is False
        assert config.max_workers == 8
        assert config.timeout_seconds == 600

    def test_orchestrator_config_validation(self):
        """Test OrchestratorConfig validation."""
        # Valid worker counts
        OrchestratorConfig(max_workers=1)
        OrchestratorConfig(max_workers=16)

        # Invalid worker counts
        with pytest.raises(ValueError):
            OrchestratorConfig(max_workers=0)

        with pytest.raises(ValueError):
            OrchestratorConfig(max_workers=17)


class TestAgentLLMConfig:
    """Tests for AgentLLMConfig model."""

    def test_agent_llm_config_defaults(self):
        """Test AgentLLMConfig default values."""
        config = AgentLLMConfig()
        assert config.llm_model == "gpt-4"
        assert config.temperature == 0.3
        assert config.max_tokens == 4096
        assert config.timeout_seconds == 60

    def test_agent_llm_config_custom_values(self):
        """Test AgentLLMConfig with custom values."""
        config = AgentLLMConfig(
            llm_model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=2048,
            timeout_seconds=30,
        )
        assert config.llm_model == "gpt-3.5-turbo"
        assert config.temperature == 0.7
        assert config.max_tokens == 2048
        assert config.timeout_seconds == 30

    def test_agent_llm_config_validation(self):
        """Test AgentLLMConfig validation."""
        # Valid temperature range
        AgentLLMConfig(temperature=0.0)
        AgentLLMConfig(temperature=2.0)

        # Invalid temperature values
        with pytest.raises(ValueError):
            AgentLLMConfig(temperature=-0.1)

        with pytest.raises(ValueError):
            AgentLLMConfig(temperature=2.1)


class TestFederalComplianceConfig:
    """Tests for FederalComplianceConfig model."""

    def test_federal_compliance_config_defaults(self):
        """Test FederalComplianceConfig default values."""
        config = FederalComplianceConfig()
        assert config.enabled is True
        assert "NIST AI RMF" in config.standards
        assert "CMMC L2" in config.standards
        assert config.oscal_export is True
        assert config.audit_trail is True
        assert config.classification == "CUI"

    def test_federal_compliance_config_custom_values(self):
        """Test FederalComplianceConfig with custom values."""
        config = FederalComplianceConfig(
            enabled=False,
            standards=["NIST 800-171"],
            oscal_export=False,
            audit_trail=False,
            classification="Public",
        )
        assert config.enabled is False
        assert config.standards == ["NIST 800-171"]
        assert config.oscal_export is False
        assert config.audit_trail is False
        assert config.classification == "Public"


class TestMLTEConfig:
    """Tests for MLTEConfig main configuration model."""

    def test_mlte_config_defaults(self):
        """Test MLTEConfig default values."""
        config = MLTEConfig()
        assert config.evaluation_enabled is True
        assert config.evaluation_mode == "synchronous"
        assert config.fail_on_error is False
        assert config.store.uri == "fs://./mlte-store"
        assert config.quality_gates.accuracy_min == 0.95
        assert config.orchestrator.max_workers == 4
        assert config.federal_compliance.enabled is True

    def test_mlte_config_custom_values(self):
        """Test MLTEConfig with custom nested values."""
        config = MLTEConfig(
            evaluation_enabled=False,
            evaluation_mode="asynchronous",
            fail_on_error=True,
            store=StoreConfig(uri="postgresql://localhost/mlte"),
            quality_gates=QualityGatesConfig(accuracy_min=0.90),
            orchestrator=OrchestratorConfig(max_workers=8),
        )
        assert config.evaluation_enabled is False
        assert config.evaluation_mode == "asynchronous"
        assert config.fail_on_error is True
        assert config.store.uri == "postgresql://localhost/mlte"
        assert config.quality_gates.accuracy_min == 0.90
        assert config.orchestrator.max_workers == 8

    def test_mlte_config_load_from_yaml(self, sample_config_yaml):
        """Test loading MLTEConfig from YAML file."""
        config = MLTEConfig.load_from_yaml(str(sample_config_yaml))

        assert config.store.uri == "fs://./test-mlte-store"
        assert config.store.connection_pool_size == 5
        assert config.evaluation_enabled is True
        assert config.evaluation_mode == "synchronous"
        assert config.quality_gates.accuracy_min == 0.90
        assert config.quality_gates.security_min == 0.85
        assert config.orchestrator.max_workers == 2
        assert config.agents["negotiation"].llm_model == "gpt-3.5-turbo"
        assert config.federal_compliance.enabled is True

    def test_mlte_config_load_from_yaml_file_not_found(self):
        """Test loading from non-existent YAML file."""
        with pytest.raises(FileNotFoundError):
            MLTEConfig.load_from_yaml("/nonexistent/config.yaml")

    def test_mlte_config_load_from_yaml_invalid(self, temp_dir):
        """Test loading from invalid YAML file."""
        invalid_yaml = temp_dir / "invalid.yaml"
        with open(invalid_yaml, "w") as f:
            f.write("invalid: yaml: content:\n  - bad")

        with pytest.raises(yaml.YAMLError):
            MLTEConfig.load_from_yaml(str(invalid_yaml))

    def test_mlte_config_load_from_env(self, sample_env_vars):
        """Test loading MLTEConfig from environment variables."""
        config = MLTEConfig.load_from_env()

        assert config.store.uri == "fs://./test-store"
        assert config.evaluation_enabled is True
        assert config.evaluation_mode == "asynchronous"
        assert config.fail_on_error is True
        assert config.federal_compliance.enabled is True

    def test_mlte_config_load_with_precedence(self, sample_config_yaml, sample_env_vars):
        """Test configuration loading with precedence: ENV > YAML."""
        config = MLTEConfig.load(str(sample_config_yaml))

        # ENV should override YAML
        assert config.store.uri == "fs://./test-store"  # From ENV
        assert config.evaluation_mode == "asynchronous"  # From ENV
        assert config.fail_on_error is True  # From ENV

    def test_mlte_config_load_defaults_only(self):
        """Test loading with only defaults (no file, no env vars)."""
        config = MLTEConfig.load()

        assert config.store.uri == "fs://./mlte-store"
        assert config.evaluation_mode == "synchronous"
        assert config.fail_on_error is False

    def test_mlte_config_load_yaml_only(self, sample_config_yaml):
        """Test loading with YAML file only."""
        # Clear any environment variables
        env_vars = [
            "MLTE_STORE_URI",
            "MLTE_ENABLE_EVALUATION",
            "MLTE_EVALUATION_MODE",
            "MLTE_FAIL_ON_ERROR",
        ]
        original = {k: os.environ.pop(k, None) for k in env_vars}

        try:
            config = MLTEConfig.load(str(sample_config_yaml))

            assert config.store.uri == "fs://./test-mlte-store"
            assert config.quality_gates.accuracy_min == 0.90
        finally:
            # Restore environment
            for k, v in original.items():
                if v is not None:
                    os.environ[k] = v

    def test_mlte_config_to_yaml(self, temp_dir):
        """Test exporting MLTEConfig to YAML file."""
        config = MLTEConfig(
            evaluation_enabled=False,
            evaluation_mode="ci_only",
            store=StoreConfig(uri="postgresql://localhost/test"),
        )

        output_path = temp_dir / "output_config.yaml"
        config.to_yaml(str(output_path))

        assert output_path.exists()

        # Load and verify
        with open(output_path, "r") as f:
            data = yaml.safe_load(f)

        assert data["mlte"]["evaluation_enabled"] is False
        assert data["mlte"]["evaluation_mode"] == "ci_only"
        assert data["mlte"]["store"]["uri"] == "postgresql://localhost/test"

    def test_mlte_config_to_yaml_creates_directory(self, temp_dir):
        """Test that to_yaml creates parent directories if needed."""
        config = MLTEConfig()

        output_path = temp_dir / "nested" / "dir" / "config.yaml"
        config.to_yaml(str(output_path))

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_mlte_config_validate_federal_requirements_valid(self):
        """Test federal requirements validation with valid config."""
        config = MLTEConfig(
            federal_compliance=FederalComplianceConfig(
                enabled=True,
                audit_trail=True,
                standards=["CMMC L2"],
            ),
            store=StoreConfig(type="postgresql"),
            quality_gates=QualityGatesConfig(security_min=0.90),
        )

        errors = config.validate_federal_requirements()
        assert len(errors) == 0

    def test_mlte_config_validate_federal_requirements_no_audit_trail(self):
        """Test validation fails when audit trail is disabled."""
        config = MLTEConfig(
            federal_compliance=FederalComplianceConfig(
                enabled=True, audit_trail=False
            )
        )

        errors = config.validate_federal_requirements()
        assert len(errors) > 0
        assert any("audit trail" in error.lower() for error in errors)

    def test_mlte_config_validate_federal_requirements_memory_store(self):
        """Test validation fails with memory store for federal compliance."""
        config = MLTEConfig(
            federal_compliance=FederalComplianceConfig(enabled=True),
            store=StoreConfig(type="memory"),
        )

        errors = config.validate_federal_requirements()
        assert len(errors) > 0
        assert any("memory store" in error.lower() for error in errors)

    def test_mlte_config_validate_federal_requirements_cmmc_security_threshold(self):
        """Test validation fails when CMMC security threshold is too low."""
        config = MLTEConfig(
            federal_compliance=FederalComplianceConfig(
                enabled=True, standards=["CMMC L2"]
            ),
            quality_gates=QualityGatesConfig(security_min=0.85),
        )

        errors = config.validate_federal_requirements()
        assert len(errors) > 0
        assert any("security threshold" in error.lower() for error in errors)

    def test_mlte_config_validate_federal_requirements_disabled(self):
        """Test validation passes when federal compliance is disabled."""
        config = MLTEConfig(
            federal_compliance=FederalComplianceConfig(
                enabled=False, audit_trail=False
            ),
            store=StoreConfig(type="memory"),
        )

        errors = config.validate_federal_requirements()
        assert len(errors) == 0

    def test_mlte_config_agent_llm_configs(self):
        """Test per-agent LLM configuration."""
        config = MLTEConfig(
            agents={
                "negotiation": AgentLLMConfig(
                    llm_model="gpt-3.5-turbo", temperature=0.5
                ),
                "testing": AgentLLMConfig(llm_model="gpt-4", temperature=0.0),
            }
        )

        assert config.agents["negotiation"].llm_model == "gpt-3.5-turbo"
        assert config.agents["negotiation"].temperature == 0.5
        assert config.agents["testing"].llm_model == "gpt-4"
        assert config.agents["testing"].temperature == 0.0

    def test_mlte_config_serialization_round_trip(self, temp_dir):
        """Test that config can be serialized and deserialized without loss."""
        original_config = MLTEConfig(
            evaluation_enabled=False,
            evaluation_mode="ci_only",
            store=StoreConfig(uri="test://store", type="http"),
            quality_gates=QualityGatesConfig(accuracy_min=0.85),
            orchestrator=OrchestratorConfig(max_workers=2),
            agents={
                "negotiation": AgentLLMConfig(llm_model="test-model"),
            },
            federal_compliance=FederalComplianceConfig(
                enabled=False, classification="Public"
            ),
        )

        # Save to file
        output_path = temp_dir / "round_trip.yaml"
        original_config.to_yaml(str(output_path))

        # Load from file
        loaded_config = MLTEConfig.load_from_yaml(str(output_path))

        # Verify all fields match
        assert loaded_config.evaluation_enabled == original_config.evaluation_enabled
        assert loaded_config.evaluation_mode == original_config.evaluation_mode
        assert loaded_config.store.uri == original_config.store.uri
        assert loaded_config.store.type == original_config.store.type
        assert (
            loaded_config.quality_gates.accuracy_min
            == original_config.quality_gates.accuracy_min
        )
        assert (
            loaded_config.orchestrator.max_workers
            == original_config.orchestrator.max_workers
        )
        assert (
            loaded_config.agents["negotiation"].llm_model
            == original_config.agents["negotiation"].llm_model
        )
        assert (
            loaded_config.federal_compliance.enabled
            == original_config.federal_compliance.enabled
        )


class TestConfigIntegration:
    """Integration tests for config functionality."""

    def test_complete_config_workflow(self, temp_dir):
        """Test complete configuration workflow."""
        # 1. Create config programmatically
        config = MLTEConfig(
            evaluation_mode="asynchronous",
            store=StoreConfig(uri="postgresql://localhost/mlte"),
            quality_gates=QualityGatesConfig(accuracy_min=0.92),
        )

        # 2. Validate federal requirements
        errors = config.validate_federal_requirements()
        assert len(errors) == 0

        # 3. Export to YAML
        yaml_path = temp_dir / "workflow.yaml"
        config.to_yaml(str(yaml_path))

        # 4. Load from YAML
        loaded_config = MLTEConfig.load_from_yaml(str(yaml_path))

        # 5. Verify loaded config matches
        assert loaded_config.evaluation_mode == "asynchronous"
        assert loaded_config.store.uri == "postgresql://localhost/mlte"
        assert loaded_config.quality_gates.accuracy_min == 0.92

    def test_config_with_all_agents(self):
        """Test configuration with all agent types configured."""
        config = MLTEConfig(
            agents={
                "negotiation": AgentLLMConfig(llm_model="gpt-4", temperature=0.3),
                "testing": AgentLLMConfig(llm_model="gpt-4", temperature=0.0),
                "validation": AgentLLMConfig(llm_model="gpt-4", temperature=0.0),
                "reporting": AgentLLMConfig(llm_model="gpt-4", temperature=0.5),
                "compliance": AgentLLMConfig(llm_model="gpt-4", temperature=0.0),
            }
        )

        assert len(config.agents) == 5
        for agent_name in [
            "negotiation",
            "testing",
            "validation",
            "reporting",
            "compliance",
        ]:
            assert agent_name in config.agents
            assert config.agents[agent_name].llm_model == "gpt-4"
