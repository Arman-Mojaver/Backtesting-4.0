import pytest

from schemas.atr_schema import AtrSchema


@pytest.fixture
def atr_data():
    return {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
        "risk": 0.02,
    }


def test_valid_atr_schema(atr_data):
    atr = AtrSchema(**atr_data)

    assert atr.type == atr_data["type"]
    assert atr.tp_multiplier == atr_data["tp_multiplier"]
    assert atr.sl_multiplier == atr_data["sl_multiplier"]
    assert atr.parameters.atr_parameter == atr_data["parameters"]["atr_parameter"]
    assert atr.risk == atr_data["risk"]
    assert atr.identifier == "atr-1.5-1.0-14-0.02"
