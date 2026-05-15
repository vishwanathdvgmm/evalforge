import pytest

from evalforge.exceptions import DuplicateRegistrationError, RegistryError
from evalforge.registry import MetricRegistry


def test_metric_registry_register_and_lookup() -> None:
    registry = MetricRegistry()

    registry.register(
        name="accuracy",
        fn=lambda value: 1.0,
        kind="rule",
    )

    metric = registry.get("accuracy")

    assert metric.name == "accuracy"


def test_metric_registry_duplicate_registration() -> None:
    registry = MetricRegistry()

    registry.register(
        name="accuracy",
        fn=lambda value: 1.0,
        kind="rule",
    )

    with pytest.raises(DuplicateRegistrationError):
        registry.register(
            name="accuracy",
            fn=lambda value: 1.0,
            kind="rule",
        )


def test_metric_registry_missing_lookup() -> None:
    registry = MetricRegistry()

    with pytest.raises(RegistryError):
        registry.get("missing")
