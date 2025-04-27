import pytest
from pydantic import ValidationError

from database.models import Indicator


@pytest.mark.parametrize(
    "invalid_macd_data",
    [
        # Missing Parameters
        {
            "type": "rsi",
            "identifier": "rsi.14",
        },
        # Missing Identifier
        {
            "type": "rsi",
            "parameters": {"n": 14},
        },
        # Empty parameters
        {
            "type": "rsi",
            "parameters": {},
            "identifier": "rsi.14",
        },
        # Missing n in parameters
        {
            "type": "rsi",
            "parameters": {"t": 14},
            "identifier": "rsi.14",
        },
        # Wrong n type
        {
            "type": "rsi",
            "parameters": {"n": "abc"},
            "identifier": "rsi.14",
        },
        # n is Negative
        {
            "type": "rsi",
            "parameters": {"n": -14},
            "identifier": "rsi.14",
        },
        # n is 0
        {
            "type": "rsi",
            "parameters": {"n": 0},
            "identifier": "rsi.14",
        },
    ],
)
def test_invalid(invalid_macd_data):
    with pytest.raises(ValidationError):
        Indicator(**invalid_macd_data)


def test_valid():
    valid_data = {
        "type": "rsi",
        "parameters": {"n": 14},
        "identifier": "rsi.14",
    }
    indicator = Indicator(**valid_data)

    assert indicator.type == valid_data["type"]
    assert indicator.parameters == valid_data["parameters"]
    assert indicator.identifier == valid_data["identifier"]
