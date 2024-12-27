from unittest.mock import patch

import pytest

from database.models import (
    LongOperationPoint,
    ShortOperationPoint,
)
from testing_utils.dict_utils import list_of_dicts_are_equal
from views.operation_points_view import OperationPointsCreateMultipleView


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("three_resampled_points_d1")
def test_create_one_pair_without_balance_overflow(
    money_management_strategies,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    money_management_strategy_1, money_management_strategy_2 = money_management_strategies

    long_operation_points_1 = (
        session.query(LongOperationPoint)
        .filter_by(money_management_strategy_id=money_management_strategy_1.id)
        .all()
    )
    long_operation_points_2 = (
        session.query(LongOperationPoint)
        .filter_by(money_management_strategy_id=money_management_strategy_2.id)
        .all()
    )
    short_operation_points_1 = (
        session.query(ShortOperationPoint)
        .filter_by(money_management_strategy_id=money_management_strategy_1.id)
        .all()
    )

    short_operation_points_2 = (
        session.query(ShortOperationPoint)
        .filter_by(money_management_strategy_id=money_management_strategy_2.id)
        .all()
    )

    # money_management_strategy_1

    long_results_1 = [i.to_dict() for i in long_operation_points_1]
    expected_long_results_1 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42],
        }
    ]

    short_results_1 = [i.to_dict() for i in short_operation_points_1]
    expected_short_results_1 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [-27, 42],
        }
    ]

    # money_management_strategy_2

    long_results_2 = [i.to_dict() for i in long_operation_points_2]
    expected_long_results_2 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -22,
            "tp": 43,
            "sl": 22,
            "long_balance": [27, -42],
        }
    ]

    short_results_2 = [i.to_dict() for i in short_operation_points_2]
    expected_short_results_2 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -22,
            "tp": 43,
            "sl": 22,
            "short_balance": [-27, 42],
        }
    ]

    assert (
        i.money_management_strategy_id == money_management_strategy_1.id
        for i in long_operation_points_1 + short_operation_points_1
    )
    assert (
        i.money_management_strategy_id == money_management_strategy_2.id
        for i in long_operation_points_2 + short_operation_points_2
    )
    assert list_of_dicts_are_equal(long_results_1, expected_long_results_1)
    assert list_of_dicts_are_equal(short_results_1, expected_short_results_1)
    assert list_of_dicts_are_equal(long_results_2, expected_long_results_2)
    assert list_of_dicts_are_equal(short_results_2, expected_short_results_2)
