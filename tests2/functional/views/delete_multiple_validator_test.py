import pytest

from views.delete_multiple_validator import DeleteMultipleValidator


def test_all_empty():
    with pytest.raises(ValueError):
        DeleteMultipleValidator(set(), []).run()


def test_empty_indicators():
    with pytest.raises(ValueError):
        DeleteMultipleValidator({"wrong_identifier"}, []).run()
