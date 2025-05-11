import pytest

from database.models import ShortOperationPoint
from utils.date_utils import string_to_datetime


@pytest.fixture
def short_operation_point_data():
    return {
        "instrument": "EURUSD",
        "datetime": "2023-08-24",
        "result": -58,
        "tp": 50,
        "sl": 30,
        "short_balance": [14, -58, -21, -98, -70, -41, -81, 29],
        "risk": 0.02,
        "timestamp": int(string_to_datetime("2023-08-24").timestamp()),
    }


@pytest.fixture
def short_operation_point(short_operation_point_data):
    return ShortOperationPoint(
        **short_operation_point_data,
        money_management_strategy_id=1,
    )


def test_to_request_format(short_operation_point):
    result = short_operation_point.to_request_format()
    assert short_operation_point.id == result["id"]
    assert (
        short_operation_point.money_management_strategy_id
        == result["money_management_strategy_id"]
    )
