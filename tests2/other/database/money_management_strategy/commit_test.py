import pytest
from sqlalchemy.exc import IntegrityError

from database.handler import DatabaseHandler
from database.models import MoneyManagementStrategy
from testing_utils.dict_utils import lists_are_equal


def test_commit_empty_items_does_nothing(session):
    DatabaseHandler(session).commit_money_management_strategies([])

    assert not session.query(MoneyManagementStrategy).all()


def test_commit_empty_items_with_existing_tables_items_does_nothing(
    other_money_management_strategies,
    session,
):
    DatabaseHandler(session).commit_money_management_strategies([])

    assert lists_are_equal(
        MoneyManagementStrategy.query.all(), other_money_management_strategies
    )


def test_commit_success_one_with_empty_table(
    money_management_strategy,
    session,
):
    DatabaseHandler(session).commit_money_management_strategies(
        [money_management_strategy]
    )

    assert lists_are_equal(
        session.query(MoneyManagementStrategy).all(), [money_management_strategy]
    )


def test_commit_success_multiple_with_empty_table(
    money_management_strategies,
    session,
):
    DatabaseHandler(session).commit_money_management_strategies(
        money_management_strategies
    )

    assert lists_are_equal(
        session.query(MoneyManagementStrategy).all(), money_management_strategies
    )


def test_commit_success_one_with_existing_tables_items(
    other_money_management_strategies,
    money_management_strategy,
    session,
):
    DatabaseHandler(session).commit_money_management_strategies(
        [money_management_strategy]
    )

    assert lists_are_equal(
        session.query(MoneyManagementStrategy).all(),
        [
            money_management_strategy,
            *other_money_management_strategies,
        ],
    )


def test_commit_success_multiple_with_existing_tables_items(
    other_money_management_strategies,
    money_management_strategies,
    session,
):
    DatabaseHandler(session).commit_money_management_strategies(
        money_management_strategies
    )

    assert lists_are_equal(
        session.query(MoneyManagementStrategy).all(),
        [
            *money_management_strategies,
            *other_money_management_strategies,
        ],
    )


@pytest.mark.usefixtures("other_money_management_strategies")
def test_commit_with_colliding_identifiers_raises_error(
    other_money_management_strategies_data,
    session,
):
    repeated_item = MoneyManagementStrategy(**other_money_management_strategies_data[0])

    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_money_management_strategies([repeated_item])
