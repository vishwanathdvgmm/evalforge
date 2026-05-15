import pytest

from evalforge.exceptions import (
    DuplicateRegistrationError,
    SuiteExecutionError,
)
from evalforge.suite import Suite
from evalforge.types import Case


def test_suite_testcase_registration() -> None:
    suite = Suite(name="demo")

    @suite.testcase
    def testcase() -> Case:
        return Case(input="What is Python?")

    assert len(suite.testcases) == 1


def test_suite_duplicate_testcase_registration() -> None:
    suite = Suite(name="demo")

    @suite.testcase
    def testcase() -> Case:
        return Case(input="What is Python?")

    with pytest.raises(DuplicateRegistrationError):
        suite.testcase(testcase)


@pytest.mark.asyncio
async def test_suite_run_without_runtime_engine() -> None:
    suite = Suite(name="demo")

    @suite.testcase
    def testcase() -> Case:
        return Case(input="What is Python?")

    with pytest.raises(SuiteExecutionError):
        await suite.run()
