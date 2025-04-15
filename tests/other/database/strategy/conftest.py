import random

import pytest

from database.models import Indicator, MoneyManagementStrategy, Strategy


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    for item in session.query(Strategy).all():
        session.delete(item)

    for item in session.query(MoneyManagementStrategy).all():
        session.delete(item)

    for item in session.query(Indicator).all():
        session.delete(item)
    session.commit()


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
def indicator_data_2():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 13, "price_target": "close"},
            "fast": {"type": "ema", "n": 5, "price_target": "close"},
        },
        "identifier": "macd.sma-13-close,ema-5-close",
    }


@pytest.fixture
def indicator_data_3():
    return {
        "type": "macd",
        "parameters": {
            "slow": {"type": "sma", "n": 14, "price_target": "close"},
            "fast": {"type": "ema", "n": 6, "price_target": "close"},
        },
        "identifier": "macd.sma-14-close,ema-6-close",
    }


@pytest.fixture
def indicator(indicator_data):
    return Indicator(id=10, **indicator_data)


@pytest.fixture
def indicator_2(indicator_data_2):
    return Indicator(id=11, **indicator_data_2)


@pytest.fixture
def indicator_3(indicator_data_3):
    return Indicator(id=12, **indicator_data_3)


@pytest.fixture
def money_management_strategy_data():
    return {
        "type": "atr",
        "tp_multiplier": 2.5,
        "sl_multiplier": 2.0,
        "parameters": {"atr_parameter": 14},
        "identifier": "atr-2.5-2.0-14",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy_data_2():
    return {
        "type": "atr",
        "tp_multiplier": 2.7,
        "sl_multiplier": 2.8,
        "parameters": {"atr_parameter": 15},
        "identifier": "atr-2.7-2.8-15",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy_data_3():
    return {
        "type": "atr",
        "tp_multiplier": 3.7,
        "sl_multiplier": 3.8,
        "parameters": {"atr_parameter": 15},
        "identifier": "atr-3.7-3.8-15",
        "risk": 0.02,
    }


@pytest.fixture
def money_management_strategy(money_management_strategy_data):
    return MoneyManagementStrategy(id=1, **money_management_strategy_data)


@pytest.fixture
def money_management_strategy_2(money_management_strategy_data_2):
    return MoneyManagementStrategy(id=2, **money_management_strategy_data_2)


@pytest.fixture
def money_management_strategy_3(money_management_strategy_data_3):
    return MoneyManagementStrategy(id=3, **money_management_strategy_data_3)


def generate_random_strategy_data():
    annual_roi = round(random.uniform(-0.2, 0.5) * 100, 2)  # noqa: S311
    max_draw_down = round(random.uniform(0.05, 0.4) * 100, 2)  # noqa: S311
    annual_operation_count = random.randint(10, 20)  # noqa: S311

    return {
        "annual_roi": annual_roi,
        "max_draw_down": max_draw_down,
        "annual_operation_count": annual_operation_count,
    }


@pytest.fixture
def strategies_data():
    return [generate_random_strategy_data() for _ in range(1)]


@pytest.fixture
def strategies(
    strategies_data,
    indicator_3,
    money_management_strategy_3,
):
    items = [Strategy(**item) for item in strategies_data]
    items[0].money_management_strategy_id = money_management_strategy_3.id
    items[0].indicator_id = indicator_3.id

    return items


@pytest.fixture
def other_strategies_data():
    return [generate_random_strategy_data() for _ in range(4)]


@pytest.fixture
def other_strategies(  # noqa: PLR0913
    other_strategies_data,
    indicator,
    indicator_2,
    money_management_strategy,
    money_management_strategy_2,
    session,
):
    items = [Strategy(**item) for item in other_strategies_data]
    items[0].money_management_strategy_id = money_management_strategy.id
    items[1].money_management_strategy_id = money_management_strategy.id
    items[2].money_management_strategy_id = money_management_strategy_2.id
    items[3].money_management_strategy_id = money_management_strategy_2.id

    items[0].indicator_id = indicator.id
    items[1].indicator_id = indicator_2.id
    items[2].indicator_id = indicator.id
    items[3].indicator_id = indicator_2.id

    session.add_all(items)
    session.commit()

    return items
