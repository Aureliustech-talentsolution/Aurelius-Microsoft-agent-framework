"""
ValidationAgent Sub-Agents

1. ValiditySubAgent - Validates test methodology and coverage
2. ValueSubAgent - Applies quality gates and thresholds
"""

from typing import List, Dict, Any, Optional
import logging
import re

from .validation import QualityGate, GateResult, Status, Severity

logger = logging.getLogger(__name__)


class ValiditySubAgent:
    """
    Validates test methodology and coverage.

    Checks:
    - Test coverage is sufficient
    - Test methodology is sound
    - No obvious biases in test data
    - Test results are reproducible
    """

    async def validate_test_validity(
        self,
        test_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        """
        Validate test methodology.

        Returns:
            List of validity issues (empty if valid)
        """
        logger.info("Validating test methodology")

        issues = []

        # Check for minimum test count
        test_count = test_results.get("test_count", 0)
        if test_count < 10:
            issues.append(f"Insufficient test coverage: {test_count} tests (minimum 10 required)")

        # Check for test diversity
        test_types = test_results.get("test_types", [])
        required_types = {"security", "performance", "accuracy"}
        missing_types = required_types - set(test_types)
        if missing_types:
            issues.append(f"Missing test types: {', '.join(missing_types)}")

        # Check for reproducibility metadata
        if "reproducibility" not in test_results:
            issues.append("Missing reproducibility metadata (seed, version, etc.)")

        # Check for statistical significance
        if "confidence_interval" not in test_results:
            issues.append("Missing confidence intervals for measurements")

        # Check for bias indicators
        if "fairness_metrics" in test_results:
            fairness = test_results["fairness_metrics"]
            if fairness.get("demographic_parity_difference", 0) > 0.20:
                issues.append("High demographic parity difference suggests biased test data")

        if issues:
            logger.warning("Found %d validity issues", len(issues))
        else:
            logger.info("Test methodology validated successfully")

        return issues


class ValueSubAgent:
    """
    Applies quality gates and thresholds.

    Evaluates each quality gate condition against test results
    and provides detailed reasoning.
    """

    def __init__(self, quality_gates: List[QualityGate]):
        """Initialize with quality gates."""
        self.quality_gates = quality_gates
        logger.info("ValueSubAgent initialized with %d gates", len(quality_gates))

    async def evaluate_gates(
        self,
        test_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]] = None,
    ) -> List[GateResult]:
        """
        Evaluate all quality gates.

        Args:
            test_results: Test execution results
            agent_spec: Optional agent specification

        Returns:
            List of GateResult for each quality gate
        """
        logger.info("Evaluating %d quality gates", len(self.quality_gates))

        gate_results = []
        for gate in self.quality_gates:
            result = await self._evaluate_single_gate(gate, test_results, agent_spec)
            gate_results.append(result)

        passed = sum(1 for r in gate_results if r.status == Status.PASS)
        logger.info("Gate evaluation complete: %d/%d passed", passed, len(gate_results))

        return gate_results

    async def _evaluate_single_gate(
        self,
        gate: QualityGate,
        test_results: Dict[str, Any],
        agent_spec: Optional[Dict[str, Any]],
    ) -> GateResult:
        """Evaluate single quality gate."""
        logger.debug("Evaluating gate: %s", gate.name)

        try:
            # Parse condition to extract metric path and comparison
            # Example: "security.prompt_injection_success_rate >= 0.95"
            metric_path, operator, threshold = self._parse_condition(gate.condition)

            # Extract measured value from test results
            measured_value = self._extract_metric(test_results, metric_path)
            if measured_value is None:
                return GateResult(
                    gate_name=gate.name,
                    status=Status.SKIPPED,
                    measured_value=None,
                    expected_value=threshold,
                    reasoning=f"Metric '{metric_path}' not found in test results",
                    severity=gate.severity,
                )

            # Evaluate condition
            passed = self._evaluate_condition(measured_value, operator, threshold)
            status = Status.PASS if passed else (Status.WARNING if gate.severity == Severity.WARNING else Status.FAIL)

            # Generate reasoning and remediation
            reasoning = self._generate_reasoning(
                gate.name, measured_value, operator, threshold, passed
            )
            remediation = None if passed else self._generate_remediation(gate, measured_value, threshold)

            return GateResult(
                gate_name=gate.name,
                status=status,
                measured_value=measured_value,
                expected_value=threshold,
                reasoning=reasoning,
                remediation=remediation,
                severity=gate.severity,
            )

        except Exception as e:
            logger.error("Error evaluating gate %s: %s", gate.name, str(e))
            return GateResult(
                gate_name=gate.name,
                status=Status.FAIL,
                measured_value=None,
                expected_value=None,
                reasoning=f"Gate evaluation error: {str(e)}",
                severity=gate.severity,
            )

    def _parse_condition(self, condition: str) -> tuple:
        """Parse gate condition into (metric_path, operator, threshold)."""
        # Example: "security.prompt_injection_success_rate >= 0.95"
        pattern = r"([\w.]+)\s*(>=|<=|>|<|==|!=)\s*([\d.]+)"
        match = re.match(pattern, condition.strip())
        if not match:
            raise ValueError(f"Invalid condition format: {condition}")

        metric_path = match.group(1)
        operator = match.group(2)
        threshold = float(match.group(3))

        return metric_path, operator, threshold

    def _extract_metric(self, test_results: Dict[str, Any], metric_path: str) -> Optional[float]:
        """Extract metric value from nested dict using dot notation."""
        parts = metric_path.split(".")
        value = test_results

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None

        return float(value) if value is not None else None

    def _evaluate_condition(self, measured: float, operator: str, threshold: float) -> bool:
        """Evaluate condition."""
        ops = {
            ">=": lambda m, t: m >= t,
            "<=": lambda m, t: m <= t,
            ">": lambda m, t: m > t,
            "<": lambda m, t: m < t,
            "==": lambda m, t: abs(m - t) < 1e-6,
            "!=": lambda m, t: abs(m - t) >= 1e-6,
        }
        return ops[operator](measured, threshold)

    def _generate_reasoning(
        self,
        gate_name: str,
        measured: float,
        operator: str,
        threshold: float,
        passed: bool,
    ) -> str:
        """Generate clear reasoning for gate result."""
        if passed:
            return f"✅ {gate_name}: Measured {measured:.4f} {operator} {threshold:.4f} (PASS)"
        else:
            gap = abs(measured - threshold)
            gap_pct = (gap / threshold * 100) if threshold != 0 else 0
            return f"❌ {gate_name}: Measured {measured:.4f}, expected {operator} {threshold:.4f} (gap: {gap:.4f}, {gap_pct:.1f}%)"

    def _generate_remediation(self, gate: QualityGate, measured: float, threshold: float) -> str:
        """Generate remediation recommendation."""
        category_remediations = {
            "security": "Strengthen input validation, add adversarial training data, implement defense-in-depth",
            "performance": "Optimize model inference, add caching, scale infrastructure",
            "accuracy": "Improve training data quality, tune hyperparameters, add validation checks",
            "fairness": "Balance training data, add fairness constraints, audit decision logic",
        }

        base_remediation = category_remediations.get(
            gate.category,
            "Review test results and adjust agent implementation",
        )

        gap = abs(measured - threshold)
        gap_pct = (gap / threshold * 100) if threshold != 0 else 0

        return f"{base_remediation} (need to improve by {gap:.4f} or {gap_pct:.1f}%)"
