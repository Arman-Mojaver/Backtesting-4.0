import pytest

from database.models import MoneyManagementStrategy
from schemas.atr_schema import AtrSchema


@pytest.fixture
def money_management_strategies_data():
    return [
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.5,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.0,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 14},
            "risk": 0.03,
        },
        {
            "type": "atr",
            "tp_multiplier": 1.6,
            "sl_multiplier": 1.1,
            "parameters": {"atr_parameter": 15},
            "risk": 0.03,
        },
    ]


@pytest.fixture
def money_management_strategy_schemas(money_management_strategies_data):
    return [AtrSchema(**item) for item in money_management_strategies_data]


@pytest.fixture
def money_management_strategies(money_management_strategy_schemas):
    return [
        MoneyManagementStrategy(**schema.model_dump())
        for schema in money_management_strategy_schemas
    ]
