from database.models import Indicator
from testing_utils.dict_utils import lists_are_equal

NON_EXISTENT_ID = 123456789
NON_EXISTENT_IDENTIFIER = "macd.sma-58-close,ema-500-close"


def test_all_with_empty_table(session):
    assert not Indicator.query.all()


def test_all_with_table_items(session, other_indicators):
    assert lists_are_equal(Indicator.query.all(), other_indicators)


def test_from_ids_with_empty_table(session):
    assert Indicator.query.from_ids(ids=set()) == []
    assert Indicator.query.from_ids(ids={NON_EXISTENT_ID}) == []


def test_from_ids_with_table_items(
    session,
    other_indicators,
):
    item_1, item_2 = other_indicators

    assert Indicator.query.from_ids(ids=set()) == []
    assert Indicator.query.from_ids(ids={NON_EXISTENT_ID}) == []
    assert lists_are_equal(Indicator.query.from_ids(ids={item_1.id}), [item_1])
    assert lists_are_equal(Indicator.query.from_ids(ids={item_2.id}), [item_2])
    assert lists_are_equal(
        Indicator.query.from_ids(ids={item_1.id, item_2.id}), other_indicators
    )
    assert lists_are_equal(
        Indicator.query.from_ids(ids={NON_EXISTENT_ID, item_1.id, item_2.id}),
        other_indicators,
    )


def test_from_identifier_with_empty_table(session):
    assert Indicator.query.from_identifiers(identifiers=set()) == []
    assert Indicator.query.from_identifiers(identifiers={NON_EXISTENT_IDENTIFIER}) == []


def test_from_identifier_with_table_items(
    session,
    other_indicators,
):
    item_1, item_2 = other_indicators

    assert Indicator.query.from_identifiers(identifiers=set()) == []
    assert Indicator.query.from_identifiers(identifiers={NON_EXISTENT_IDENTIFIER}) == []
    assert lists_are_equal(
        Indicator.query.from_identifiers(identifiers={item_1.identifier}), [item_1]
    )
    assert lists_are_equal(
        Indicator.query.from_identifiers(identifiers={item_2.identifier}), [item_2]
    )
    assert lists_are_equal(
        Indicator.query.from_identifiers(
            identifiers={item_1.identifier, item_2.identifier}
        ),
        other_indicators,
    )
    assert lists_are_equal(
        Indicator.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER, item_1.identifier, item_2.identifier}
        ),
        other_indicators,
    )
