from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from database.models import MoneyManagementStrategy
from fixtures.helpers import generate_identifier
from views.money_management_strategy.delete_multiple_view import (
    MoneyManagementStrategyDeleteMultipleView,
    NonExistentIdentifierError,
)


@pytest.fixture
def money_management_strategies(session):
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
    }

    money_management_strategy_data_2 = {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 15},
    }

    money_management_strategy_1 = MoneyManagementStrategy(
        **money_management_strategy_data_1,
        identifier=generate_identifier(money_management_strategy_data_1),
    )
    money_management_strategy_2 = MoneyManagementStrategy(
        **money_management_strategy_data_2,
        identifier=generate_identifier(money_management_strategy_data_2),
    )

    session.add_all([money_management_strategy_1, money_management_strategy_2])
    session.commit()

    yield [
        money_management_strategy_1,
        money_management_strategy_2,
    ]

    session.query(MoneyManagementStrategy).delete()
    session.commit()


def test_empty_table_returns_error(session):
    MoneyManagementStrategyDeleteMultipleView().run()

    assert session.query(MoneyManagementStrategy).all() == []


@pytest.mark.usefixtures("money_management_strategies")
def test_wrong_identifier_returns_error():
    with pytest.raises(NonExistentIdentifierError):
        MoneyManagementStrategyDeleteMultipleView(identifiers={"wrong_identifier"}).run()


def test_partial_wrong_identifiers_returns_error(money_management_strategies):
    identifiers = [item.identifier for item in money_management_strategies]
    with pytest.raises(NonExistentIdentifierError):
        MoneyManagementStrategyDeleteMultipleView(
            identifiers={"wrong_identifier", *identifiers},
        ).run()


@pytest.mark.usefixtures("money_management_strategies")
def test_non_existent_identifiers_returns_error():
    non_existent_valid_identifier = "atr-1000.1-2000.4-5000"
    with pytest.raises(NonExistentIdentifierError):
        MoneyManagementStrategyDeleteMultipleView(
            identifiers={non_existent_valid_identifier},
        ).run()


def test_partial_non_existent_identifiers_returns_error(money_management_strategies):
    identifiers = [item.identifier for item in money_management_strategies]
    non_existent_valid_identifier = "atr-1000.1-2000.4-5000"
    with pytest.raises(NonExistentIdentifierError):
        MoneyManagementStrategyDeleteMultipleView(
            identifiers={non_existent_valid_identifier, *identifiers},
        ).run()


@pytest.mark.usefixtures("money_management_strategies")
def test_empty_identifiers_delete_all(session):
    MoneyManagementStrategyDeleteMultipleView().run()

    assert not session.query(MoneyManagementStrategy).all()


def test_delete_multiple_by_identifiers(money_management_strategies, session):
    identifiers = {item.identifier for item in money_management_strategies}
    MoneyManagementStrategyDeleteMultipleView(identifiers=identifiers).run()

    assert not session.query(MoneyManagementStrategy).all()


def test_delete_partial_multiple_by_identifiers(money_management_strategies, session):
    money_management_strategy_1, money_management_strategy_2 = money_management_strategies
    MoneyManagementStrategyDeleteMultipleView(
        identifiers={money_management_strategy_1.identifier}
    ).run()

    assert session.query(MoneyManagementStrategy).all() == [money_management_strategy_2]


@patch("views.money_management_strategy.delete_multiple_view.session")
def test_commit_error(mock_session):
    mock_session.commit.side_effect = SQLAlchemyError

    with pytest.raises(SQLAlchemyError):
        MoneyManagementStrategyDeleteMultipleView().run()
