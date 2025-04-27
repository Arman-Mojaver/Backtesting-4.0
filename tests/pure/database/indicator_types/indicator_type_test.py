import pytest

from database.models import Indicator


@pytest.mark.parametrize(
    "invalid_data",
    [
        # Invalid "type"
        {
            "type": "wrong type",
            "parameters": {
                "slow": {"type": "sma", "n": -12, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
        # Missing "type"
        {
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
    ],
)
def test_invalid_type(invalid_data):
    with pytest.raises(TypeError):
        Indicator(**invalid_data)
