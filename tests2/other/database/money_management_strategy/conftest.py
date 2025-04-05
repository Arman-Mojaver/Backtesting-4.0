import pytest

from database.models import MoneyManagementStrategy


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    session.query(MoneyManagementStrategy).delete()
    session.commit()


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
    return MoneyManagementStrategy(**money_management_strategy_data)


@pytest.fixture
def money_management_strategies_data():
    return [
        {
            "type": "atr",
            "tp_multiplier": 2.5,
            "sl_multiplier": 2.0,
            "parameters": {"atr_parameter": 14},
            "identifier": "atr-2.5-2.0-14",
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 2.7,
            "sl_multiplier": 2.8,
            "parameters": {"atr_parameter": 15},
            "identifier": "atr-2.7-2.8-15",
            "risk": 0.02,
        },
    ]


@pytest.fixture
def money_management_strategies(money_management_strategies_data):
    return [MoneyManagementStrategy(**item) for item in money_management_strategies_data]


@pytest.fixture
def other_money_management_strategies_data():
    return [
        {
            "type": "atr",
            "tp_multiplier": 3.5,
            "sl_multiplier": 3.0,
            "parameters": {"atr_parameter": 14},
            "identifier": "atr-3.5-3.0-14",
            "risk": 0.02,
        },
        {
            "type": "atr",
            "tp_multiplier": 3.7,
            "sl_multiplier": 3.8,
            "parameters": {"atr_parameter": 15},
            "identifier": "atr-3.7-3.8-15",
            "risk": 0.02,
        },
    ]


@pytest.fixture
def other_money_management_strategies(
    other_money_management_strategies_data,
    session,
):
    items = [
        MoneyManagementStrategy(**item) for item in other_money_management_strategies_data
    ]

    session.add_all(items)
    session.commit()

    yield items

    session.query(MoneyManagementStrategy).delete()
