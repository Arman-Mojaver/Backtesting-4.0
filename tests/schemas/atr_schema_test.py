import pytest
from pydantic import ValidationError

from schemas.atr_schema import AtrSchema


@pytest.fixture
def atr_data():
    return {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
    }


def test_valid_atr_schema(atr_data):
    atr = AtrSchema(**atr_data)

    assert atr.type == atr_data["type"]
    assert atr.tp_multiplier == atr_data["tp_multiplier"]
    assert atr.sl_multiplier == atr_data["sl_multiplier"]
    assert atr.parameters.atr_parameter == atr_data["parameters"]["atr_parameter"]
    assert atr.identifier == "atr-1.5-1.0-14"


@pytest.mark.parametrize(
    "invalid_data",
    [
        {
            "type": 123,  # Invalid: type must be a string
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
        },
        {
            "type": "atr",
            "tp_multiplier": -1.5,  # Invalid: must be greater than 0
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": -0.5,  # Invalid: must be greater than 0
            "parameters": {"atr_parameter": 14},
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": "fourteen"},  # Invalid: must be an integer
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {},  # Invalid: empty parameters
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            # Missing "parameters"
        },
    ],
)
def test_invalid_schemas(invalid_data):
    with pytest.raises(ValidationError):
        AtrSchema(**invalid_data)
