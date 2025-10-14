"""
Configuration management for MLTE integration.

This module provides configuration management using Pydantic models
with support for YAML files and environment variable overrides.

Federal Compliance:
- CM-6 (Configuration Settings)
- CM-7 (Least Functionality)
- Audit-ready configuration tracking
"""

import os
from pathlib import Path
from typing import Dict, List, Literal, Optional

import yaml
from pydantic import BaseModel, Field


class StoreConfig(BaseModel):
    """
    MLTE store configuration.

    Attributes:
        uri: Store URI (fs://, postgresql://, http://)
        type: Store backend type
        connection_pool_size: Connection pool size for RDBS

    Federal Compliance:
        - CM-6: Configuration settings documentation
        - SC-8: Transmission confidentiality (TLS in URI)
    """

    uri: str = Field(default="fs://./mlte-store", description="MLTE store URI")
    type: Literal["filesystem", "postgresql", "memory", "http"] = "filesystem"
    connection_pool_size: int = Field(default=10, ge=1, le=100)


class QualityGatesConfig(BaseModel):
    """
    Quality gate thresholds.

    Attributes:
        accuracy_min: Minimum accuracy threshold (0.0-1.0)
        security_min: Minimum security threshold (0.0-1.0)
        latency_max_ms: Maximum latency threshold (milliseconds)
        memory_max_mb: Maximum memory usage threshold (megabytes)

    Federal Compliance:
        - Enforces quality standards for federal deployments
    """

    accuracy_min: float = Field(default=0.95, ge=0.0, le=1.0)
    security_min: float = Field(default=0.90, ge=0.0, le=1.0)
    latency_max_ms: int = Field(default=2000, ge=1)
    memory_max_mb: int = Field(default=512, ge=1)


class OrchestratorConfig(BaseModel):
    """
    Orchestrator configuration.

    Attributes:
        parallel_execution: Enable parallel agent execution
        max_workers: Maximum parallel workers
        timeout_seconds: Evaluation timeout

    Federal Compliance:
        - Resource management per SC-5 (Denial of Service Protection)
    """

    parallel_execution: bool = True
    max_workers: int = Field(default=4, ge=1, le=16)
    timeout_seconds: int = Field(default=300, ge=1)


class AgentLLMConfig(BaseModel):
    """
    LLM configuration for evaluation agents.

    Attributes:
        llm_model: Model identifier
        temperature: Sampling temperature
        max_tokens: Maximum tokens per response
        timeout_seconds: Request timeout

    Federal Compliance:
        - IA-4: Identifier management
    """

    llm_model: str = "gpt-4"
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1)
    timeout_seconds: int = Field(default=60, ge=1)


class FederalComplianceConfig(BaseModel):
    """
    Federal compliance configuration.

    Attributes:
        enabled: Enable federal compliance agent
        standards: List of compliance standards to check
        oscal_export: Enable OSCAL document export
        audit_trail: Enable detailed audit trail
        classification: Data classification level

    Federal Compliance:
        - CA-2: Security Assessments
        - CA-7: Continuous Monitoring
        - Implements NIST AI RMF and CMMC requirements
    """

    enabled: bool = True
    standards: List[str] = Field(default_factory=lambda: ["NIST AI RMF", "CMMC L2"])
    oscal_export: bool = True
    audit_trail: bool = True
    classification: Literal["CUI", "Public", "Confidential"] = "CUI"


class MLTEConfig(BaseModel):
    """
    Main MLTE configuration.

    This is the root configuration object that contains all settings
    for MLTE integration.

    Attributes:
        store: Store configuration
        evaluation_enabled: Enable/disable evaluation
        evaluation_mode: Evaluation execution mode
        fail_on_error: Raise exception on evaluation failure
        quality_gates: Quality gate thresholds
        orchestrator: Orchestrator settings
        agents: Per-agent LLM configurations
        federal_compliance: Federal compliance settings

    Federal Compliance:
        - CM-6: Complete configuration management
        - Supports CMMC L2 configuration requirements

    Example:
        >>> config = MLTEConfig.load("config.yaml")
        >>> config.store.uri
        'postgresql://...'
    """

    store: StoreConfig = Field(default_factory=StoreConfig)
    evaluation_enabled: bool = True
    evaluation_mode: Literal["synchronous", "asynchronous", "ci_only"] = "synchronous"
    fail_on_error: bool = False
    quality_gates: QualityGatesConfig = Field(default_factory=QualityGatesConfig)
    orchestrator: OrchestratorConfig = Field(default_factory=OrchestratorConfig)
    agents: Dict[str, AgentLLMConfig] = Field(default_factory=dict)
    federal_compliance: FederalComplianceConfig = Field(
        default_factory=FederalComplianceConfig
    )

    @classmethod
    def load_from_yaml(cls, path: str) -> "MLTEConfig":
        """
        Load configuration from YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            MLTEConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is malformed

        Federal Compliance:
            - CM-6: Configuration from documented sources
        """
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(config_path, "r") as f:
            data = yaml.safe_load(f)

        mlte_data = data.get("mlte", {})
        return cls(**mlte_data)

    @classmethod
    def load_from_env(cls) -> "MLTEConfig":
        """
        Load configuration from environment variables.

        Environment variables:
            MLTE_STORE_URI: Store URI
            MLTE_ENABLE_EVALUATION: Enable evaluation (true/false)
            MLTE_EVALUATION_MODE: Evaluation mode
            MLTE_FAIL_ON_ERROR: Fail on error (true/false)
            ENABLE_FEDERAL_COMPLIANCE_AGENT: Enable compliance agent

        Returns:
            MLTEConfig instance with env overrides

        Federal Compliance:
            - CM-6: Environment-based configuration
        """
        return cls(
            store=StoreConfig(
                uri=os.getenv("MLTE_STORE_URI", "fs://./mlte-store"),
            ),
            evaluation_enabled=os.getenv("MLTE_ENABLE_EVALUATION", "true").lower()
            == "true",
            evaluation_mode=os.getenv("MLTE_EVALUATION_MODE", "synchronous"),  # type: ignore
            fail_on_error=os.getenv("MLTE_FAIL_ON_ERROR", "false").lower() == "true",
            federal_compliance=FederalComplianceConfig(
                enabled=os.getenv("ENABLE_FEDERAL_COMPLIANCE_AGENT", "true").lower()
                == "true",
            ),
        )

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "MLTEConfig":
        """
        Load configuration with precedence: CLI > ENV > YAML > Defaults.

        Args:
            config_path: Optional path to YAML config file

        Returns:
            MLTEConfig instance

        Federal Compliance:
            - CM-6: Hierarchical configuration with documented precedence

        Example:
            >>> # Load with defaults
            >>> config = MLTEConfig.load()
            >>>
            >>> # Load from file with env overrides
            >>> config = MLTEConfig.load(".aurelius/mlte-config.yaml")
        """
        # Start with defaults
        config = cls()

        # Override with YAML if provided
        if config_path and Path(config_path).exists():
            config = cls.load_from_yaml(config_path)

        # Override with environment variables
        env_config = cls.load_from_env()
        merged_dict = {
            **config.model_dump(exclude_unset=True),
            **env_config.model_dump(exclude_unset=True),
        }

        return cls(**merged_dict)

    def to_yaml(self, path: str) -> None:
        """
        Export configuration to YAML file.

        Args:
            path: Output file path

        Federal Compliance:
            - CM-6: Configuration documentation
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        config_dict = {"mlte": self.model_dump(mode="json")}

        with open(output_path, "w") as f:
            yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)

    def validate_federal_requirements(self) -> List[str]:
        """
        Validate configuration meets federal requirements.

        Returns:
            List of validation errors (empty if valid)

        Federal Compliance:
            - Validates CMMC L2 configuration requirements
            - Ensures audit trail is enabled for federal deployments
        """
        errors = []

        if self.federal_compliance.enabled:
            if not self.federal_compliance.audit_trail:
                errors.append("Audit trail must be enabled for federal compliance")

            if self.store.type == "memory":
                errors.append("Memory store not allowed for federal compliance")

            if "CMMC" in " ".join(self.federal_compliance.standards):
                if self.quality_gates.security_min < 0.90:
                    errors.append("CMMC requires security threshold >= 0.90")

        return errors
