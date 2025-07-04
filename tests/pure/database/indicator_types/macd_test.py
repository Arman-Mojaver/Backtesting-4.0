import pytest
from pydantic import ValidationError

from database.models import Indicator


@pytest.mark.parametrize(
    "invalid_macd_data",
    [
        # Missing "parameters.fast"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close",
        },
        # Missing "parameters.slow"
        {
            "type": "macd",
            "parameters": {
                "fast": {"type": "ema", "n": -5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close",
        },
        # Missing "identifier"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
        },
        # Invalid "type" in "parameters.slow"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "wrong", "n": 12, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
        # Invalid "type" in "parameters.fast"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "close"},
                "fast": {"type": "wrong", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
        # Invalid "n" in "parameters.slow"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": -12, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
        # Invalid "n" in "parameters.fast"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "close"},
                "fast": {"type": "ema", "n": -5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
        # Invalid "price_target" in "parameters.slow"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "wrong"},
                "fast": {"type": "ema", "n": 5, "price_target": "close"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
        # Invalid "price_target" in "parameters.fast"
        {
            "type": "macd",
            "parameters": {
                "slow": {"type": "sma", "n": 12, "price_target": "close"},
                "fast": {"type": "ema", "n": 5, "price_target": "wrong"},
            },
            "identifier": "macd.sma-12-close,ema-5-close",
        },
    ],
)
def test_invalid(invalid_macd_data):
    with pytest.raises(ValidationError):
        Indicator(**invalid_macd_data)


def test_valid():
    valid_data = {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-12-close,ema-5-close",
    }
    indicator = Indicator(**valid_data)

    assert indicator.type == valid_data["type"]
    assert indicator.parameters == valid_data["parameters"]
    assert indicator.identifier == valid_data["identifier"]
