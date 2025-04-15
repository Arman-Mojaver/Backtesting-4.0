import pytest
from sqlalchemy.exc import IntegrityError

from database.handler import DatabaseHandler
from database.models import Strategy
from testing_utils.set_utils import set_of_tuples


def test_commit_success_multiple_with_empty_table(other_strategies, session):
    DatabaseHandler(session).commit_strategies(other_strategies)

    assert set_of_tuples(session.query(Strategy).all()) == set_of_tuples(other_strategies)


def test_commit_success_multiple_with_existing_table(
    strategies,
    other_strategies,
    session,
):
    DatabaseHandler(session).commit_strategies(strategies)

    assert set_of_tuples(session.query(Strategy).all()) == set_of_tuples(
        [*strategies, *other_strategies]
    )


def test_commit_with_colliding_identifiers_raises_error(
    other_strategies,
    session,
):
    point_data = other_strategies[0]
    repeated_point = Strategy(**point_data.to_dict())
    repeated_point.money_management_strategy_id = point_data.money_management_strategy_id
    repeated_point.indicator_id = point_data.indicator_id

    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_strategies([repeated_point])
