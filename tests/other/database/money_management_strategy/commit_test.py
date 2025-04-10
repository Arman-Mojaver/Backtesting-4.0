import pytest
from sqlalchemy.exc import IntegrityError

from database.handler import DatabaseHandler
from database.models import MoneyManagementStrategy
from testing_utils.set_utils import set_of_tuples


def test_commit_success_multiple_with_empty_table(
    money_management_strategies,
    session,
):
    DatabaseHandler(session).commit_money_management_strategies(
        money_management_strategies
    )

    assert set_of_tuples(session.query(MoneyManagementStrategy).all()) == set_of_tuples(
        money_management_strategies
    )


def test_commit_success_multiple_with_existing_tables_items(
    other_money_management_strategies,
    money_management_strategies,
    session,
):
    DatabaseHandler(session).commit_money_management_strategies(
        money_management_strategies
    )

    assert set_of_tuples(session.query(MoneyManagementStrategy).all()) == set_of_tuples(
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
