import pytest

from database.models import Indicator


@pytest.fixture
def indicators_data():
    return [
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 13, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-13-close,ema-5-close",
        },
    ]


@pytest.fixture
def indicators(indicators_data):
    return [Indicator(**indicator_data) for indicator_data in indicators_data]
