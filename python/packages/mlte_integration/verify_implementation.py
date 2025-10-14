#!/usr/bin/env python3
"""
Quick verification script for MLTE integration implementation.

This script validates that the types and configuration system work correctly
without requiring the full test suite to run.

Federal Compliance: Validation per CMMC CA.L2-3.12.4
"""

import sys
from pathlib import Path

def verify_types():
    """Verify type definitions work correctly."""
    print("=" * 60)
    print("Verifying Type Definitions")
    print("=" * 60)

    from agent_framework_mlte_integration.types import (
        AgentSpec,
        QualityGate,
        GateResult,
        EvaluationStatus,
        EvaluationReport,
        ComplianceReport,
        NIST_AI_RMF_CHARACTERISTICS,
        CMMC_LEVEL_2_DOMAINS,
    )

    # Test AgentSpec
    print("\n1. Testing AgentSpec...")
    agent_spec = AgentSpec(
        model_id="test_agent",
        version="1.0.0",
        name="Test Agent",
        description="Test agent for verification",
        tools=[{"name": "test_tool"}],
    )
    assert agent_spec.model_id == "test_agent"
    print("   ✓ AgentSpec creation successful")

    # Test validation
    try:
        AgentSpec(model_id="", version="1.0.0", name="Test", description="Test")
        print("   ✗ Validation should have failed!")
        return False
    except ValueError:
        print("   ✓ AgentSpec validation works")

    # Test QualityGate
    print("\n2. Testing QualityGate...")
    gate = QualityGate(
        name="Test Gate",
        test_case_id="test",
        threshold=0.95,
        comparison=">=",
        severity="critical",
        blocking=True,
    )
    assert gate.evaluate(0.96) is True
    assert gate.evaluate(0.94) is False
    print("   ✓ QualityGate evaluation works")

    # Test GateResult
    print("\n3. Testing GateResult...")
    result = GateResult(
        passed=[gate],
        failed=[],
        blocking_failures=[],
        deployment_allowed=True,
    )
    assert result.pass_rate == 1.0
    assert "PASSED" in result.summary
    print("   ✓ GateResult metrics work")

    # Test EvaluationReport
    print("\n4. Testing EvaluationReport...")
    report = EvaluationReport(
        agent_spec=agent_spec,
        status=EvaluationStatus.COMPLETED,
        gate_result=result,
    )
    assert report.is_complete is True
    assert report.is_passed is True
    report_dict = report.to_dict()
    assert report_dict["agent"]["model_id"] == "test_agent"
    print("   ✓ EvaluationReport serialization works")

    # Test ComplianceReport
    print("\n5. Testing ComplianceReport...")
    compliance = ComplianceReport(
        nist_ai_rmf={
            "Valid and Reliable": ["accuracy"],
            "Safe": ["robustness"],
        },
        cmmc_controls={
            "AC.L2-3.1.1": ["access_control"],
        },
    )
    assert 0 < compliance.nist_ai_rmf_coverage < 1
    assert compliance.cmmc_coverage == 1.0
    print("   ✓ ComplianceReport coverage calculations work")

    # Test constants
    print("\n6. Testing Constants...")
    assert len(NIST_AI_RMF_CHARACTERISTICS) == 7
    assert len(CMMC_LEVEL_2_DOMAINS) == 16
    print("   ✓ Constants defined correctly")

    print("\n" + "=" * 60)
    print("✓ All type definitions verified successfully!")
    print("=" * 60)
    return True


def verify_config():
    """Verify configuration management works correctly."""
    print("\n\n" + "=" * 60)
    print("Verifying Configuration Management")
    print("=" * 60)

    from agent_framework_mlte_integration.config import (
        MLTEConfig,
        StoreConfig,
        QualityGatesConfig,
        FederalComplianceConfig,
    )

    # Test default config
    print("\n1. Testing default configuration...")
    config = MLTEConfig()
    assert config.store.uri == "fs://./mlte-store"
    assert config.evaluation_enabled is True
    assert config.quality_gates.accuracy_min == 0.95
    print("   ✓ Default configuration created")

    # Test custom config
    print("\n2. Testing custom configuration...")
    custom_config = MLTEConfig(
        evaluation_mode="asynchronous",
        store=StoreConfig(uri="postgresql://localhost/test"),
        quality_gates=QualityGatesConfig(accuracy_min=0.90),
    )
    assert custom_config.evaluation_mode == "asynchronous"
    assert custom_config.store.uri == "postgresql://localhost/test"
    assert custom_config.quality_gates.accuracy_min == 0.90
    print("   ✓ Custom configuration works")

    # Test validation
    print("\n3. Testing validation...")
    try:
        QualityGatesConfig(accuracy_min=1.5)  # Invalid
        print("   ✗ Validation should have failed!")
        return False
    except ValueError:
        print("   ✓ Config validation works")

    # Test federal compliance validation
    print("\n4. Testing federal compliance validation...")
    federal_config = MLTEConfig(
        federal_compliance=FederalComplianceConfig(
            enabled=True,
            audit_trail=True,
        ),
        store=StoreConfig(type="postgresql"),
    )
    errors = federal_config.validate_federal_requirements()
    assert len(errors) == 0
    print("   ✓ Federal compliance validation passed")

    # Test with errors
    print("\n5. Testing federal compliance error detection...")
    invalid_federal_config = MLTEConfig(
        federal_compliance=FederalComplianceConfig(
            enabled=True,
            audit_trail=False,  # Should fail
        )
    )
    errors = invalid_federal_config.validate_federal_requirements()
    assert len(errors) > 0
    print(f"   ✓ Detected {len(errors)} validation error(s)")

    # Test YAML loading (if config file exists)
    print("\n6. Testing YAML configuration loading...")
    config_path = Path(".aurelius/mlte-config.yaml")
    if config_path.exists():
        yaml_config = MLTEConfig.load_from_yaml(str(config_path))
        assert yaml_config.store.uri is not None
        print("   ✓ YAML configuration loaded successfully")
    else:
        print("   ⓘ YAML config file not found (expected in some environments)")

    print("\n" + "=" * 60)
    print("✓ All configuration features verified successfully!")
    print("=" * 60)
    return True


def verify_integration():
    """Verify types and config work together."""
    print("\n\n" + "=" * 60)
    print("Verifying Integration")
    print("=" * 60)

    from agent_framework_mlte_integration.config import MLTEConfig, QualityGatesConfig
    from agent_framework_mlte_integration.types import AgentSpec, QualityGate

    print("\n1. Testing config-driven quality gates...")
    config = MLTEConfig(
        quality_gates=QualityGatesConfig(
            accuracy_min=0.95,
            security_min=0.90,
            latency_max_ms=2000,
        )
    )

    # Create quality gates from config
    gates = [
        QualityGate(
            name="Accuracy",
            test_case_id="accuracy",
            threshold=config.quality_gates.accuracy_min,
            comparison=">=",
            severity="critical",
            blocking=True,
        ),
        QualityGate(
            name="Security",
            test_case_id="security",
            threshold=config.quality_gates.security_min,
            comparison=">=",
            severity="critical",
            blocking=True,
        ),
        QualityGate(
            name="Latency",
            test_case_id="latency",
            threshold=config.quality_gates.latency_max_ms,
            comparison="<=",
            severity="high",
            blocking=False,
        ),
    ]

    assert len(gates) == 3
    assert gates[0].threshold == 0.95
    assert gates[1].threshold == 0.90
    assert gates[2].threshold == 2000
    print("   ✓ Quality gates created from config")

    print("\n2. Testing complete workflow...")
    agent_spec = AgentSpec(
        model_id="integration_test_agent",
        version="1.0.0",
        name="Integration Test Agent",
        description="Testing integration between types and config",
    )

    # Simulate evaluation
    results = {
        "accuracy": 0.96,  # Pass
        "security": 0.92,  # Pass
        "latency": 1800,  # Pass
    }

    passed = []
    failed = []
    for gate in gates:
        test_id = gate.test_case_id
        if test_id in results and gate.evaluate(results[test_id]):
            passed.append(gate)
        else:
            failed.append(gate)

    assert len(passed) == 3
    assert len(failed) == 0
    print("   ✓ All quality gates passed")

    print("\n" + "=" * 60)
    print("✓ Integration verified successfully!")
    print("=" * 60)
    return True


def main():
    """Run all verification checks."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  MLTE Integration Implementation Verification            ║")
    print("║  Version: 0.1.0                                          ║")
    print("║  Aurelius Tech & Talent Solutions                        ║")
    print("╚" + "=" * 58 + "╝")

    try:
        # Run verifications
        types_ok = verify_types()
        config_ok = verify_config()
        integration_ok = verify_integration()

        # Summary
        print("\n\n" + "╔" + "=" * 58 + "╗")
        print("║  VERIFICATION SUMMARY                                    ║")
        print("╠" + "=" * 58 + "╣")
        print(f"║  Type Definitions:      {'✓ PASSED' if types_ok else '✗ FAILED':<40} ║")
        print(f"║  Configuration:         {'✓ PASSED' if config_ok else '✗ FAILED':<40} ║")
        print(f"║  Integration:           {'✓ PASSED' if integration_ok else '✗ FAILED':<40} ║")
        print("╠" + "=" * 58 + "╣")

        if types_ok and config_ok and integration_ok:
            print("║  RESULT: ✓ ALL CHECKS PASSED                            ║")
            print("╚" + "=" * 58 + "╝")
            print("\n✓ MLTE integration implementation verified successfully!")
            print("✓ Ready to proceed with Phase 2: Core Agents Implementation\n")
            return 0
        else:
            print("║  RESULT: ✗ SOME CHECKS FAILED                           ║")
            print("╚" + "=" * 58 + "╝")
            print("\n✗ Verification failed. Please review errors above.\n")
            return 1

    except Exception as e:
        print("\n\n" + "=" * 60)
        print("✗ VERIFICATION FAILED WITH EXCEPTION")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
