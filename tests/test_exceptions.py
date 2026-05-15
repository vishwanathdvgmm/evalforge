from evalforge.exceptions import EvalForgeError, ValidationError


def test_validation_error_is_evalforge_error() -> None:
    assert issubclass(ValidationError, EvalForgeError)
