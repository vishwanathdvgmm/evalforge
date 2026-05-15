from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any

from evalforge.exceptions import ValidationError
from evalforge.registry import metric_registry

SUPPORTED_PROVIDERS = frozenset({"anthropic", "gemini", "ollama"})

MetricFunction = Callable[..., float]


def _validate_metric_signature(fn: Callable[..., Any]) -> None:
    signature = inspect.signature(fn)

    if not signature.parameters:
        raise ValidationError(f"Metric '{fn.__name__}' must accept at least one parameter.")


def metric(fn: MetricFunction) -> MetricFunction:
    """Register a rule-based metric."""

    _validate_metric_signature(fn)

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> float:
        result = fn(*args, **kwargs)

        if not isinstance(result, (float, int)):
            raise ValidationError(f"Metric '{fn.__name__}' must return a float-compatible value.")

        return float(result)

    metric_registry.register(
        name=fn.__name__,
        fn=wrapper,
        kind="rule",
        metadata={},
    )

    wrapper.__evalforge_metric__ = True
    wrapper.__evalforge_kind__ = "rule"

    return wrapper


def judge(
    *,
    provider: str,
    model: str,
    threshold: float,
) -> Callable[[MetricFunction], MetricFunction]:
    """Register an LLM-as-judge metric."""

    provider_normalized = provider.strip().lower()

    if provider_normalized not in SUPPORTED_PROVIDERS:
        raise ValidationError(f"Unsupported provider '{provider}'.")

    if not model.strip():
        raise ValidationError("Judge model name cannot be empty.")

    if not 0.0 <= threshold <= 1.0:
        raise ValidationError("Judge threshold must be between 0.0 and 1.0.")

    def decorator(fn: MetricFunction) -> MetricFunction:
        _validate_metric_signature(fn)

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            result = fn(*args, **kwargs)

            if not isinstance(result, (float, int)):
                raise ValidationError(
                    f"Judge metric '{fn.__name__}' must return a float-compatible value."
                )

            return float(result)

        metadata = {
            "provider": provider_normalized,
            "model": model,
            "threshold": threshold,
        }

        metric_registry.register(
            name=fn.__name__,
            fn=wrapper,
            kind="judge",
            metadata=metadata,
        )

        wrapper.__evalforge_metric__ = True
        wrapper.__evalforge_kind__ = "judge"
        wrapper.__evalforge_provider__ = provider_normalized
        wrapper.__evalforge_model__ = model
        wrapper.__evalforge_threshold__ = threshold

        return wrapper

    return decorator
