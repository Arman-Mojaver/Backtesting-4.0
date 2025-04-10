from database.handler import DatabaseHandler
from database.models import MoneyManagementStrategy
from testing_utils.set_utils import set_of_tuples


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

    assert set_of_tuples(MoneyManagementStrategy.query.all()) == set_of_tuples([item_2])
