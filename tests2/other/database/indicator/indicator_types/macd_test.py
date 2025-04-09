import pytest

from database.models import Indicator


@pytest.fixture
def valid_macd_data():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-12-close,ema-5-close",
    }


def test_valid(valid_macd_data, session):
    indicator = Indicator(**valid_macd_data)

    session.add(indicator)
    session.commit()

    assert indicator.id
    assert indicator.to_dict() == valid_macd_data

    session.delete(indicator)
    session.commit()
