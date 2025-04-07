from database.handler import DatabaseHandler
from database.models import MoneyManagementStrategy
from testing_utils.dict_utils import lists_are_equal


def test_delete_empty_items_does_nothing(session):
    DatabaseHandler(session).delete_money_management_strategies([])

    assert not session.query(MoneyManagementStrategy).all()


def test_delete_empty_items_with_existing_tables_items_does_nothing(
    other_money_management_strategies,
    session,
):
    DatabaseHandler(session).delete_money_management_strategies([])

    assert lists_are_equal(
        MoneyManagementStrategy.query.all(), other_money_management_strategies
    )


def test_delete_all_existing_items(
    other_money_management_strategies,
    session,
):
    DatabaseHandler(session).delete_money_management_strategies(
        other_money_management_strategies
    )

    assert not MoneyManagementStrategy.query.all()


def test_delete_partial_existing_items(
    other_money_management_strategies,
    session,
):
    item_1, item_2 = other_money_management_strategies
    DatabaseHandler(session).delete_money_management_strategies([item_1])

    assert lists_are_equal(MoneyManagementStrategy.query.all(), [item_2])
