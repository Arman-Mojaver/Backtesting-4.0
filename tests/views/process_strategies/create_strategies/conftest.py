import pytest

from database.models import Indicator, MoneyManagementStrategy


@pytest.fixture
def strategy_response_defaults():
    def _defaults(overrides=None):
        values = {
            "long_operation_point_ids": [],
            "short_operation_point_ids": [],
            "strategy_data": {
                "annual_roi": 10.0,
                "annual_operation_count": 0.5,
                "max_draw_down": 2.0,
                "indicator_id": 1,
                "money_management_strategy_id": 1,
            },
        }
        if overrides:
            values.update(overrides)
        return values

    return _defaults


@pytest.fixture
def indicator_data():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 12, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-12-close,ema-5-close",
    }


@pytest.fixture
def indicator(indicator_data, session):
    return Indicator(id=10, **indicator_data)


@pytest.fixture
def money_management_strategy_data():
    return {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
        "identifier": "atr-1.5-1.0-14",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy(money_management_strategy_data):
    return MoneyManagementStrategy(id=1, **money_management_strategy_data)


@pytest.fixture
def money_management_strategies():
    money_management_strategy_data_1 = {
        "type": "atr",
        "tp_multiplier": 1.5,
        "sl_multiplier": 1.0,
        "parameters": {"atr_parameter": 14},
        "identifier": "atr-1.5-1.0-14",
        "risk": 0.02,
    }

    money_management_strategy_data_2 = {
        "type": "atr",
        "tp_multiplier": 1.7,
        "sl_multiplier": 0.8,
        "parameters": {"atr_parameter": 15},
        "identifier": "atr-1.7-0.8-15",
        "risk": 0.02,
    }

    point_1 = MoneyManagementStrategy(id=5, **money_management_strategy_data_1)
    point_2 = MoneyManagementStrategy(id=6, **money_management_strategy_data_2)

    return [point_1, point_2]
