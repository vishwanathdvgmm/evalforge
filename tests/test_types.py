import pytest

from evalforge.exceptions import ValidationError
from evalforge.types import Case, Dataset


def test_case_creation() -> None:
    case = Case(input="What is Python?")

    assert case.input == "What is Python?"


def test_case_invalid_input() -> None:
    with pytest.raises(ValidationError):
        Case(input="")


def test_dataset_iteration() -> None:
    dataset = Dataset(cases=[Case(input="A"), Case(input="B")])

    assert len(dataset) == 2
    assert dataset[0].input == "A"


def test_dataset_rejects_invalid_objects() -> None:
    with pytest.raises(ValidationError):
        Dataset(cases=["invalid"])
