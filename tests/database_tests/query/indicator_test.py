import pytest

from database.models import Indicator, MoneyManagementStrategy
from testing_utils.dict_utils import lists_are_equal


@pytest.fixture
def points(session):
    indicator_data_1 = {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "sma-12-close-ema-5-close",
    }

    indicator_data_2 = {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 13, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "sma-13-close-ema-5-close",
    }

    indicator_1 = Indicator(**indicator_data_1)
    indicator_2 = Indicator(**indicator_data_2)

    session.add_all([indicator_1, indicator_2])
    session.commit()

    yield [indicator_1, indicator_2]

    session.delete(indicator_1)
    session.delete(indicator_2)
    session.commit()


def test_all(session, points):
    assert lists_are_equal(MoneyManagementStrategy.query.all(), points)
