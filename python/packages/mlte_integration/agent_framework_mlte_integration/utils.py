"""
Utility functions for MLTE integration.

This module provides common utility functions used throughout
the MLTE integration package.

Federal Compliance:
- AU-12: Audit generation support
- SI-11: Error handling
"""

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

import structlog

# Setup structured logging
logger = structlog.get_logger(__name__)


def generate_artifact_id(prefix: str, data: Dict[str, Any]) -> str:
    """
    Generate unique artifact ID from data.

    Args:
        prefix: Artifact type prefix (e.g., "card", "test", "report")
        data: Data to hash for uniqueness

    Returns:
        Unique artifact identifier

    Federal Compliance:
        - IA-4: Identifier management
        - AU-12: Audit record generation

    Example:
        >>> data = {"model": "MyAgent", "version": "v1.0.0"}
        >>> artifact_id = generate_artifact_id("card", data)
        >>> artifact_id.startswith("card_")
        True
    """
    data_str = json.dumps(data, sort_keys=True)
    hash_value = hashlib.sha256(data_str.encode()).hexdigest()[:12]
    timestamp = int(time.time())
    return f"{prefix}_{timestamp}_{hash_value}"


def format_timestamp(timestamp: Optional[float] = None) -> str:
    """
    Format timestamp for display.

    Args:
        timestamp: Unix timestamp (default: current time)

    Returns:
        ISO 8601 formatted timestamp

    Example:
        >>> ts = format_timestamp(1697000000.0)
        >>> "2023-10-11" in ts
        True
    """
    if timestamp is None:
        timestamp = time.time()
    from datetime import datetime

    return datetime.fromtimestamp(timestamp).isoformat()


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize input text for security.

    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text

    Raises:
        ValueError: If input contains potentially malicious content

    Federal Compliance:
        - SI-10: Information input validation
        - SC-24: Fail in known state

    Example:
        >>> safe_text = sanitize_input("Hello, world!")
        >>> safe_text
        'Hello, world!'
    """
    # Check length
    if len(text) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length}")

    # Check for common injection patterns
    malicious_patterns = [
        "<script>",
        "javascript:",
        "onerror=",
        "onclick=",
        "onload=",
        "eval(",
        "exec(",
    ]

    text_lower = text.lower()
    for pattern in malicious_patterns:
        if pattern in text_lower:
            raise ValueError(f"Potentially malicious pattern detected: {pattern}")

    return text


def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists, create if needed.

    Args:
        path: Directory path

    Returns:
        Path object

    Federal Compliance:
        - CM-6: Configuration management
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def load_json_file(path: str) -> Dict[str, Any]:
    """
    Load JSON file with error handling.

    Args:
        path: JSON file path

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is malformed

    Federal Compliance:
        - SI-11: Error handling
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with open(file_path, "r") as f:
        return json.load(f)


def save_json_file(data: Dict[str, Any], path: str, indent: int = 2) -> None:
    """
    Save data to JSON file.

    Args:
        data: Data to save
        path: Output file path
        indent: JSON indentation

    Federal Compliance:
        - CM-6: Configuration management
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent, sort_keys=True)


def log_audit_event(
    event_type: str,
    agent_id: str,
    user_id: str,
    action: str,
    result: str,
    **kwargs: Any,
) -> None:
    """
    Log audit event with structured logging.

    Args:
        event_type: Type of event (e.g., "agent_evaluation")
        agent_id: Agent identifier
        user_id: User identifier
        action: Action performed
        result: Action result
        **kwargs: Additional event data

    Federal Compliance:
        - AU-2: Audit events
        - AU-3: Content of audit records
        - AU-12: Audit generation

    Example:
        >>> log_audit_event(
        ...     event_type="agent_evaluation",
        ...     agent_id="WeatherAgent:v1.0.0",
        ...     user_id="user@example.com",
        ...     action="run_evaluation",
        ...     result="success",
        ...     classification="CUI"
        ... )
    """
    logger.info(
        event_type,
        agent_id=agent_id,
        user_id=user_id,
        action=action,
        result=result,
        timestamp=time.time(),
        **kwargs,
    )


def calculate_coverage(passed: int, total: int) -> float:
    """
    Calculate coverage percentage.

    Args:
        passed: Number of passed items
        total: Total number of items

    Returns:
        Coverage percentage (0.0-1.0)

    Example:
        >>> coverage = calculate_coverage(8, 10)
        >>> coverage
        0.8
    """
    if total == 0:
        return 0.0
    return passed / total


def format_duration(seconds: float) -> str:
    """
    Format duration for display.

    Args:
        seconds: Duration in seconds

    Returns:
        Human-readable duration

    Example:
        >>> format_duration(125.5)
        '2m 5.5s'
        >>> format_duration(45.2)
        '45.2s'
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds:.1f}s"


def merge_metadata(*metadata_dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple metadata dictionaries.

    Args:
        *metadata_dicts: Variable number of metadata dictionaries

    Returns:
        Merged metadata dictionary

    Example:
        >>> m1 = {"a": 1, "b": 2}
        >>> m2 = {"b": 3, "c": 4}
        >>> merge_metadata(m1, m2)
        {'a': 1, 'b': 3, 'c': 4}
    """
    result: Dict[str, Any] = {}
    for metadata in metadata_dicts:
        result.update(metadata)
    return result


class TimingContext:
    """
    Context manager for timing operations.

    Federal Compliance:
        - AU-3: Content of audit records (includes duration)

    Example:
        >>> with TimingContext("evaluation") as timer:
        ...     # perform evaluation
        ...     pass
        >>> timer.duration
        0.001234
    """

    def __init__(self, operation_name: str):
        """
        Initialize timing context.

        Args:
            operation_name: Name of operation to time
        """
        self.operation_name = operation_name
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.duration: float = 0.0

    def __enter__(self) -> "TimingContext":
        """Start timing."""
        self.start_time = time.time()
        logger.debug(f"Starting {self.operation_name}")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Stop timing and log."""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        logger.info(
            f"Completed {self.operation_name}",
            duration_seconds=self.duration,
            duration_formatted=format_duration(self.duration),
        )


def validate_version_string(version: str) -> bool:
    """
    Validate version string format.

    Args:
        version: Version string to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_version_string("v1.0.0")
        True
        >>> validate_version_string("invalid")
        False
    """
    import re

    # Semantic versioning pattern
    pattern = r"^v?\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$"
    return bool(re.match(pattern, version))


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text

    Example:
        >>> truncate_string("Hello, world!" * 10, 20)
        'Hello, world!Hel...'
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
