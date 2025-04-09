import pytest

from database.models import MoneyManagementStrategy, ShortOperationPoint
from testing_utils.dict_utils import lists_are_equal


@pytest.fixture
def money_management_strategies(session):
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

    point_1 = MoneyManagementStrategy(**money_management_strategy_data_1)
    point_2 = MoneyManagementStrategy(**money_management_strategy_data_2)

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


@pytest.fixture
def short_operation_points(money_management_strategies, session):
    money_management_strategy_1, money_management_strategy_2 = money_management_strategies
    short_operation_point_data_1 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-24",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.02,
    }

    short_operation_point_data_2 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-24",
        "result": 14,
        "tp": 10,
        "sl": 35,
        "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.02,
    }

    point_1 = ShortOperationPoint(
        **short_operation_point_data_1,
        money_management_strategy_id=money_management_strategy_1.id,
    )

    point_2 = ShortOperationPoint(
        **short_operation_point_data_2,
        money_management_strategy_id=money_management_strategy_2.id,
    )

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


def test_all(short_operation_points, session):
    assert lists_are_equal(ShortOperationPoint.query.all(), short_operation_points)
