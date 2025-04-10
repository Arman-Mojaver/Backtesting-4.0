from database.models import Indicator
from testing_utils.dict_utils import lists_are_equal

NON_EXISTENT_ID = 123456789
NON_EXISTENT_IDENTIFIER = "macd.sma-58-close,ema-500-close"


def test_all_with_empty_table(session):
    assert not Indicator.query.all()


def test_all_with_table_items(session, other_indicators):
    assert lists_are_equal(Indicator.query.all(), other_indicators)


def test_from_ids_with_empty_table(session):
    assert Indicator.query.from_ids(ids=set()).all() == []
    assert Indicator.query.from_ids(ids={NON_EXISTENT_ID}).all() == []


def test_from_ids_with_table_items(
    session,
    other_indicators,
):
    item_1, item_2 = other_indicators

    assert Indicator.query.from_ids(ids=set()).all() == []
    assert Indicator.query.from_ids(ids={NON_EXISTENT_ID}).all() == []
    assert lists_are_equal(Indicator.query.from_ids(ids={item_1.id}).all(), [item_1])
    assert lists_are_equal(Indicator.query.from_ids(ids={item_2.id}).all(), [item_2])
    assert lists_are_equal(
        Indicator.query.from_ids(ids={item_1.id, item_2.id}).all(), other_indicators
    )
    assert lists_are_equal(
        Indicator.query.from_ids(ids={NON_EXISTENT_ID, item_1.id, item_2.id}).all(),
        other_indicators,
    )


def test_from_identifier_with_empty_table(session):
    assert Indicator.query.from_identifiers(identifiers=set()).all() == []
    assert (
        Indicator.query.from_identifiers(identifiers={NON_EXISTENT_IDENTIFIER}).all()
        == []
    )


def test_from_identifier_with_table_items(
    session,
    other_indicators,
):
    item_1, item_2 = other_indicators

    assert Indicator.query.from_identifiers(identifiers=set()).all() == []
    assert (
        Indicator.query.from_identifiers(identifiers={NON_EXISTENT_IDENTIFIER}).all()
        == []
    )
    assert lists_are_equal(
        Indicator.query.from_identifiers(identifiers={item_1.identifier}).all(), [item_1]
    )
    assert lists_are_equal(
        Indicator.query.from_identifiers(identifiers={item_2.identifier}).all(), [item_2]
    )
    assert lists_are_equal(
        Indicator.query.from_identifiers(
            identifiers={item_1.identifier, item_2.identifier}
        ).all(),
        other_indicators,
    )
    assert lists_are_equal(
        Indicator.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER, item_1.identifier, item_2.identifier}
        ).all(),
        other_indicators,
    )
