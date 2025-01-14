import pytest

from database.models import MoneyManagementStrategy, ShortOperationPoint


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
def money_management_strategy(money_management_strategy_data, session):
    point = MoneyManagementStrategy(**money_management_strategy_data)

    session.add(point)
    session.commit()

    yield point

    session.delete(point)
    session.commit()


@pytest.fixture
def short_operation_point_data():
    return {
        "instrument": "EURUSD",
        "datetime": "2023-08-24",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
    }


def test_create_point(short_operation_point_data, money_management_strategy, session):
    point = ShortOperationPoint(
        **short_operation_point_data,
        money_management_strategy_id=money_management_strategy.id,
    )

    session.add(point)
    session.commit()

    assert point.id
    assert point.to_dict() == short_operation_point_data

    session.delete(point)
    session.commit()
