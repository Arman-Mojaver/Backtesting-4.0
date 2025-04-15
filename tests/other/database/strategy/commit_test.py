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
