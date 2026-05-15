from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from evalforge.exceptions import ValidationError

MetricCallable = Callable[..., float]


@dataclass(frozen=True, slots=True)
class Case:
    input: str
    expected: str | None = None
    context: str | None = None
    output: str | None = None
    metrics: tuple[MetricCallable, ...] = field(default_factory=tuple)
    metadata: MappingProxyType[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not isinstance(self.input, str) or not self.input.strip():
            raise ValidationError("Case input must be a non-empty string.")

        for metric in self.metrics:
            if not callable(metric):
                raise ValidationError("All metrics attached to a Case must be callable.")

        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )


class Dataset(Iterable[Case]):
    """Immutable dataset container."""

    def __init__(
        self,
        cases: Iterable[Case],
        *,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        validated_cases = tuple(cases)

        if not validated_cases:
            raise ValidationError("Dataset cannot be empty.")

        for case in validated_cases:
            if not isinstance(case, Case):
                raise ValidationError("Dataset accepts only Case instances.")

        self._cases = validated_cases
        self.name = name
        self.metadata = MappingProxyType(metadata or {})

    def __iter__(self) -> Iterator[Case]:
        return iter(self._cases)

    def __getitem__(self, index: int) -> Case:
        return self._cases[index]

    def __len__(self) -> int:
        return len(self._cases)
