from database.handler import DatabaseHandler
from database.models import Indicator
from testing_utils.dict_utils import lists_are_equal


def test_delete_empty_items_does_nothing(session):
    DatabaseHandler(session).delete_indicators([])

    assert not session.query(Indicator).all()


def test_delete_empty_items_with_existing_tables_items_does_nothing(
    other_indicators,
    session,
):
    DatabaseHandler(session).delete_indicators([])

    assert lists_are_equal(Indicator.query.all(), other_indicators)


def test_delete_all_existing_items(other_indicators, session):
    DatabaseHandler(session).delete_indicators(other_indicators)

    assert not Indicator.query.all()


def test_delete_partial_existing_items(other_indicators, session):
    item_1, item_2 = other_indicators
    DatabaseHandler(session).delete_indicators([item_1])

    assert lists_are_equal(Indicator.query.all(), [item_2])
