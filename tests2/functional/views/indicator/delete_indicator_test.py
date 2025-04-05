import pytest

from views.delete_multiple_validator import DeleteMultipleValidator


def test_empty_identifiers(indicators):
    with pytest.raises(ValueError):
        DeleteMultipleValidator(
            set(),
            indicators,
        ).run()


def test_greater_identifiers_set(indicators):
    existing_identifiers = {item.identifier for item in indicators}
    valid_non_existing_identifier = "macd.sma-50-close,ema-500-close"

    with pytest.raises(ValueError):
        DeleteMultipleValidator(
            {*existing_identifiers, valid_non_existing_identifier},
            indicators,
        ).run()


def test_greater_money_management_strategies_set(indicators):
    identifiers = {indicators[0].identifier}  # only first identifier

    with pytest.raises(ValueError):
        DeleteMultipleValidator(
            identifiers,
            indicators,
        ).run()


def test_success(indicators):
    identifiers = {item.identifier for item in indicators}

    assert DeleteMultipleValidator(identifiers, indicators).run() == indicators
