import pytest

from views.delete_multiple_validator import DeleteMultipleValidator


def test_empty_identifiers(money_management_strategies):
    assert (
        DeleteMultipleValidator(
            set(),
            money_management_strategies,
        ).run()
        == money_management_strategies
    )


def test_greater_identifiers_set(money_management_strategies):
    existing_identifiers = {item.identifier for item in money_management_strategies}
    valid_non_existing_identifier = "atr-1000.1-2000.4-5000"

    with pytest.raises(ValueError):
        DeleteMultipleValidator(
            {*existing_identifiers, valid_non_existing_identifier},
            money_management_strategies,
        ).run()


def test_greater_money_management_strategies_set(money_management_strategies):
    identifiers = {money_management_strategies[0].identifier}  # only first identifier

    with pytest.raises(ValueError):
        DeleteMultipleValidator(
            identifiers,
            money_management_strategies,
        ).run()


def test_success(money_management_strategies):
    identifiers = {item.identifier for item in money_management_strategies}

    assert (
        DeleteMultipleValidator(
            identifiers,
            money_management_strategies,
        ).run()
        == money_management_strategies
    )
