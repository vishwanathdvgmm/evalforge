from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from threading import RLock
from typing import Any

from evalforge.exceptions import (
    DuplicateRegistrationError,
    RegistryError,
)


@dataclass(frozen=True, slots=True)
class MetricDefinition:
    name: str
    fn: Callable[..., float]
    kind: str
    metadata: dict[str, Any]


@dataclass(frozen=True, slots=True)
class EvaluatorDefinition:
    name: str
    evaluator: type[Any]


class MetricRegistry:
    """Thread-safe registry for metrics."""

    def __init__(self) -> None:
        self._metrics: dict[str, MetricDefinition] = {}
        self._lock = RLock()

    def register(
        self,
        *,
        name: str,
        fn: Callable[..., float],
        kind: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        with self._lock:
            if name in self._metrics:
                raise DuplicateRegistrationError(f"Metric '{name}' is already registered.")

            self._metrics[name] = MetricDefinition(
                name=name,
                fn=fn,
                kind=kind,
                metadata=metadata or {},
            )

    def get(self, name: str) -> MetricDefinition:
        try:
            return self._metrics[name]
        except KeyError as error:
            raise RegistryError(f"Metric '{name}' is not registered.") from error

    def exists(self, name: str) -> bool:
        return name in self._metrics

    def list(self) -> tuple[MetricDefinition, ...]:
        return tuple(self._metrics.values())


class EvaluatorRegistry:
    """Thread-safe registry for evaluators."""

    def __init__(self) -> None:
        self._evaluators: dict[str, EvaluatorDefinition] = {}
        self._lock = RLock()

    def register(self, *, name: str, evaluator: type[Any]) -> None:
        with self._lock:
            if name in self._evaluators:
                raise DuplicateRegistrationError(f"Evaluator '{name}' is already registered.")

            self._evaluators[name] = EvaluatorDefinition(
                name=name,
                evaluator=evaluator,
            )

    def get(self, name: str) -> EvaluatorDefinition:
        try:
            return self._evaluators[name]
        except KeyError as error:
            raise RegistryError(f"Evaluator '{name}' is not registered.") from error

    def exists(self, name: str) -> bool:
        return name in self._evaluators

    def list(self) -> tuple[EvaluatorDefinition, ...]:
        return tuple(self._evaluators.values())


metric_registry = MetricRegistry()
evaluator_registry = EvaluatorRegistry()
