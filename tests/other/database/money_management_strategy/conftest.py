import pytest

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ShortOperationPoint,
)


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    for item in session.query(MoneyManagementStrategy).all():
        session.delete(item)
    session.commit()


@pytest.fixture
def money_management_strategy(money_management_strategy_data):
    return MoneyManagementStrategy(**money_management_strategy_data)


@pytest.fixture
def money_management_strategy_2(money_management_strategy_data_2):
    return MoneyManagementStrategy(**money_management_strategy_data_2)


@pytest.fixture
def money_management_strategies(money_management_strategy, money_management_strategy_2):
    return [money_management_strategy, money_management_strategy_2]


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

    return items


@pytest.fixture
def long_operation_points_data():
    return [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-25",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
    ]


@pytest.fixture
def long_op_points(long_operation_points_data):
    return [
        LongOperationPoint(**long_operation_point_data)
        for long_operation_point_data in long_operation_points_data
    ]


@pytest.fixture
def long_operation_points_data_2():
    return [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-26",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-27",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
    ]


@pytest.fixture
def long_op_points_2(long_operation_points_data_2):
    return [LongOperationPoint(**item) for item in long_operation_points_data_2]


@pytest.fixture
def other_money_management_strategies_with_long_operation_points(
    other_money_management_strategies_data,
    long_op_points,
    long_op_points_2,
    session,
):
    items = [
        MoneyManagementStrategy(**item) for item in other_money_management_strategies_data
    ]
    items[0].long_operation_points = long_op_points
    items[1].long_operation_points = long_op_points_2

    session.add_all(items)
    session.commit()

    return items


@pytest.fixture
def short_operation_points_data():
    return [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-25",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
    ]


@pytest.fixture
def short_op_points(short_operation_points_data):
    return [ShortOperationPoint(**item) for item in short_operation_points_data]


@pytest.fixture
def short_operation_points_data_2():
    return [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-26",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-27",
            "result": -58,
            "tp": 50,
            "sl": 30,
            "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
            "risk": 0.03,
        },
    ]


@pytest.fixture
def short_op_points_2(short_operation_points_data_2):
    return [ShortOperationPoint(**item) for item in short_operation_points_data_2]


@pytest.fixture
def other_money_management_strategies_with_short_operation_points(
    other_money_management_strategies_data,
    short_op_points,
    short_op_points_2,
    session,
):
    items = [
        MoneyManagementStrategy(**item) for item in other_money_management_strategies_data
    ]
    items[0].short_operation_points = short_op_points
    items[1].short_operation_points = short_op_points_2

    session.add_all(items)
    session.commit()

    return items
