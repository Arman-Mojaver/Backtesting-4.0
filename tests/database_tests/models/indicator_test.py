import pytest
from sqlalchemy.exc import IntegrityError

from database.models.indicator import Indicator


@pytest.fixture
def indicator_data():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-12-close,ema-5-close",
    }


def test_create_indicator(indicator_data, session):
    indicator = Indicator(**indicator_data)

    session.add(indicator)
    session.commit()

    assert indicator.id
    assert indicator.to_dict() == indicator_data

    session.delete(indicator)
    session.commit()


@pytest.fixture
def indicator_point(indicator_data, session):
    indicator = Indicator(**indicator_data)

    session.add(indicator)
    session.commit()

    return indicator


def test_delete_indicator(indicator_point, session):
    indicator_id = indicator_point.id

    indicator_point.delete()
    session.commit()

    assert not session.query(Indicator).filter_by(id=indicator_id).one_or_none()


def test_unique_identifier(indicator_data, session):
    indicator_1 = Indicator(**indicator_data)
    indicator_2 = Indicator(**indicator_data)

    session.add_all([indicator_1, indicator_2])

    with pytest.raises(IntegrityError):
        session.commit()
