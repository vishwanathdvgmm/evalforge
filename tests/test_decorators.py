import pytest

from evalforge.decorators import judge, metric
from evalforge.exceptions import ValidationError


@metric
def accuracy(output: str) -> float:
    return 1.0


@judge(
    provider="anthropic",
    model="claude-sonnet-4-6",
    threshold=0.7,
)
def faithfulness(output: str) -> float:
    return 0.9


def test_metric_execution() -> None:
    assert accuracy("hello") == 1.0


def test_judge_execution() -> None:
    assert faithfulness("hello") == 0.9


def test_invalid_threshold() -> None:
    with pytest.raises(ValidationError):

        @judge(
            provider="anthropic",
            model="claude",
            threshold=2.0,
        )
        def invalid_metric(output: str) -> float:
            return 0.0
