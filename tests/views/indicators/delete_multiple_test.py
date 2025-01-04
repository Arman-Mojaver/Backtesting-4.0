from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from database.models import Indicator
from views.indicator.delete_multiple_view import (
    IndicatorDeleteMultipleView,
    NonExistentIdentifierError,
)


@pytest.fixture
def indicators(session):
    indicator_data_1 = {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-12-close,ema-5-close",
    }

    indicator_data_2 = {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 13, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-13-close,ema-5-close",
    }

    indicator_1 = Indicator(**indicator_data_1)
    indicator_2 = Indicator(**indicator_data_2)

    session.add_all([indicator_1, indicator_2])
    session.commit()

    yield [indicator_1, indicator_2]

    session.query(Indicator).delete()
    session.commit()


def test_empty_table_returns_empty_list(session):
    IndicatorDeleteMultipleView().run()

    assert session.query(Indicator).all() == []


@pytest.mark.usefixtures("indicators")
def test_wrong_identifier_returns_error():
    with pytest.raises(NonExistentIdentifierError):
        IndicatorDeleteMultipleView(identifiers={"wrong_identifier"}).run()


def test_partial_wrong_identifiers_returns_error(indicators):
    identifiers = [item.identifier for item in indicators]
    with pytest.raises(NonExistentIdentifierError):
        IndicatorDeleteMultipleView(
            identifiers={"wrong_identifier", *identifiers},
        ).run()


@pytest.mark.usefixtures("indicators")
def test_non_existent_identifiers_returns_error():
    non_existent_valid_identifier = "atr-1000.1-2000.4-5000"
    with pytest.raises(NonExistentIdentifierError):
        IndicatorDeleteMultipleView(
            identifiers={non_existent_valid_identifier},
        ).run()


def test_partial_non_existent_identifiers_returns_error(indicators):
    identifiers = [item.identifier for item in indicators]
    non_existent_valid_identifier = "macd.sma-120-close,ema-500-close"
    with pytest.raises(NonExistentIdentifierError):
        IndicatorDeleteMultipleView(
            identifiers={non_existent_valid_identifier, *identifiers},
        ).run()


@pytest.mark.usefixtures("indicators")
def test_empty_identifiers_delete_all(session):
    IndicatorDeleteMultipleView().run()

    assert not session.query(Indicator).all()


def test_delete_multiple_by_identifiers(indicators, session):
    identifiers = {item.identifier for item in indicators}
    IndicatorDeleteMultipleView(identifiers=identifiers).run()

    assert not session.query(Indicator).all()


def test_delete_partial_multiple_by_identifiers(indicators, session):
    indicator_1, indicator_2 = indicators
    IndicatorDeleteMultipleView(identifiers={indicator_1.identifier}).run()

    assert session.query(Indicator).all() == [indicator_2]


@patch("views.indicator.delete_multiple_view.session")
def test_commit_error(mock_session):
    mock_session.commit.side_effect = SQLAlchemyError

    with pytest.raises(SQLAlchemyError):
        IndicatorDeleteMultipleView().run()
