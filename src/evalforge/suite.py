from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from evalforge.exceptions import (
    DuplicateRegistrationError,
    SuiteExecutionError,
    ValidationError,
)
from evalforge.types import Case, Dataset


@dataclass(frozen=True, slots=True)
class RegisteredTestCase:
    name: str
    factory: Callable[[], Case]


class Suite:
    """Primary evaluation suite abstraction."""

    def __init__(
        self,
        *,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not name.strip():
            raise ValidationError("Suite name cannot be empty.")

        self.name = name
        self.metadata = metadata or {}
        self._testcases: list[RegisteredTestCase] = []
        self._registered_names: set[str] = set()

    def testcase(
        self,
        fn: Callable[[], Case],
    ) -> Callable[[], Case]:
        testcase_name = fn.__name__

        if testcase_name in self._registered_names:
            raise DuplicateRegistrationError(
                f"Testcase '{testcase_name}' is already registered in suite '{self.name}'."
            )

        @wraps(fn)
        def wrapper() -> Case:
            case = fn()

            if not isinstance(case, Case):
                raise ValidationError(f"Testcase '{testcase_name}' must return a Case instance.")

            return case

        self._registered_names.add(testcase_name)
        self._testcases.append(RegisteredTestCase(name=testcase_name, factory=wrapper))

        return wrapper

    @property
    def testcases(self) -> tuple[RegisteredTestCase, ...]:
        return tuple(self._testcases)

    def build_dataset(self) -> Dataset:
        cases = tuple(testcase.factory() for testcase in self._testcases)
        return Dataset(cases=cases, name=self.name)

    async def run(self) -> None:
        if not self._testcases:
            raise SuiteExecutionError(f"Suite '{self.name}' contains no registered testcases.")

        raise SuiteExecutionError(
            "Runtime engine is not yet implemented. " "Execution support begins in Phase 3."
        )
