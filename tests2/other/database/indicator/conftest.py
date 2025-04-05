import pytest

from database.models import Indicator


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    session.query(Indicator).delete()
    session.commit()


@pytest.fixture
def other_indicators(session):
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
