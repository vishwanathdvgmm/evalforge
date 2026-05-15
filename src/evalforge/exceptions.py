from __future__ import annotations


class EvalForgeError(Exception):
    """Base exception for all evalforge errors."""


class RegistryError(EvalForgeError):
    """Raised when registry operations fail."""


class DuplicateRegistrationError(RegistryError):
    """Raised when attempting to register a duplicate object."""


class ValidationError(EvalForgeError):
    """Raised when validation constraints are violated."""


class ProviderError(EvalForgeError):
    """Raised for provider runtime failures."""


class SuiteExecutionError(EvalForgeError):
    """Raised when suite execution cannot proceed."""


class MetricExecutionError(EvalForgeError):
    """Raised when metric execution fails."""
