import pytest

from database.models import LongOperationPoint, MoneyManagementStrategy


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    session.query(LongOperationPoint).delete()
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
def money_management_strategy(money_management_strategy_data, session):
    money_management_strategy = MoneyManagementStrategy(**money_management_strategy_data)

    session.add(money_management_strategy)
    session.commit()

    return money_management_strategy


@pytest.fixture
def long_operation_point_data():
    return {
        "instrument": "EURUSD",
        "datetime": "2023-08-23",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.02,
    }


@pytest.fixture
def long_operation_point(money_management_strategy, long_operation_point_data, session):
    return LongOperationPoint(
        **long_operation_point_data,
        money_management_strategy_id=money_management_strategy.id,
    )


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
def long_operation_points(money_management_strategy, long_operation_points_data):
    return [
        LongOperationPoint(
            **long_operation_point_data,
            money_management_strategy_id=money_management_strategy.id,
        )
        for long_operation_point_data in long_operation_points_data
    ]


@pytest.fixture
def other_long_operation_points(money_management_strategy, session):
    point_data_1 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-26",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.04,
    }

    point_data_2 = {
        "instrument": "EURUSD",
        "datetime": "2023-08-27",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.04,
    }

    point_1 = LongOperationPoint(
        **point_data_1,
        money_management_strategy_id=money_management_strategy.id,
    )

    point_2 = LongOperationPoint(
        **point_data_2,
        money_management_strategy_id=money_management_strategy.id,
    )

    points = [point_1, point_2]

    session.add_all(points)
    session.commit()

    return points
