from database.handler import DatabaseHandler
from database.models import MoneyManagementStrategy
from testing_utils.dict_utils import lists_are_equal


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
