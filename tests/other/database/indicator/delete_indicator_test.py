from database.handler import DatabaseHandler
from database.models import Indicator
from testing_utils.set_utils import set_of_tuples


def test_delete_empty_items_does_nothing(session):
    DatabaseHandler(session).delete_indicators([])

    assert session.query(Indicator).all() == []


def test_delete_empty_items_with_existing_tables_items_does_nothing(
    other_indicators,
    session,
):
    DatabaseHandler(session).delete_indicators([])

    assert set_of_tuples(Indicator.query.all()) == set_of_tuples(other_indicators)


def test_delete_all_existing_items(other_indicators, session):
    DatabaseHandler(session).delete_indicators(other_indicators)

    assert Indicator.query.all() == []


def test_delete_partial_existing_items(other_indicators, session):
    item_1, item_2 = other_indicators
    DatabaseHandler(session).delete_indicators([item_1])

    assert set_of_tuples(Indicator.query.all()) == set_of_tuples([item_2])
