import pytest

from database.models import LongOperationPoint


@pytest.fixture
def long_operation_point_data():
    return {
        "instrument": "EURUSD",
        "datetime": "2023-08-24",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "long_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.02,
    }


@pytest.fixture
def long_operation_point(long_operation_point_data):
    return LongOperationPoint(
        **long_operation_point_data,
        money_management_strategy_id=1,
    )


def test_to_request_format(long_operation_point):
    result = long_operation_point.to_request_format()
    assert long_operation_point.id == result["id"]
    assert (
        long_operation_point.money_management_strategy_id
        == result["money_management_strategy_id"]
    )
