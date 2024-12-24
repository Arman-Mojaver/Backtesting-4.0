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
def test_create_one_pair_of_operation_points(
    money_management_strategy,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    long_operation_points = session.query(LongOperationPoint).all()
    short_operation_points = session.query(ShortOperationPoint).all()

    assert len(long_operation_points) == 1
    assert len(short_operation_points) == 1

    long_operation_point = long_operation_points[0]
    short_operation_point = session.query(ShortOperationPoint).all()[0]

    assert (
        long_operation_point.money_management_strategy_id == money_management_strategy.id
    )
    assert (
        short_operation_point.money_management_strategy_id == money_management_strategy.id
    )

    assert long_operation_point.to_dict() == {
        "instrument": "EURUSD",
        "datetime": "2023-08-23",
        "result": -14,
        "tp": 29,
        "sl": 14,
        "long_balance": [
            int(round(10000 * (-1.08448 + 1.08715))),  #  27
            int(round(10000 * (-1.08448 + 1.08026))),  # -42
        ],
    }

    assert short_operation_point.to_dict() == {
        "instrument": "EURUSD",
        "datetime": "2023-08-23",
        "result": -14,
        "tp": 29,
        "sl": 14,
        "short_balance": [
            -int(round(10000 * (-1.08448 + 1.08715))),  # -27
            -int(round(10000 * (-1.08448 + 1.08026))),  #  42
        ],
    }


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD",))
@pytest.mark.usefixtures("four_resampled_points_d1")
def test_create_two_pairs_of_operation_points(
    money_management_strategy,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    long_operation_points = session.query(LongOperationPoint).all()
    short_operation_points = session.query(ShortOperationPoint).all()

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [
                int(round(10000 * (-1.08448 + 1.08715))),  #  27
                int(round(10000 * (-1.08448 + 1.08026))),  # -42
                int(round(10000 * (-1.08448 + 1.08767))),  #  32
                int(round(10000 * (-1.08448 + 1.0805))),  # -40
            ],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -16,
            "tp": 32,
            "sl": 16,
            "long_balance": [
                int(round(10000 * (-1.08631 + 1.08767))),  #  14
                int(round(10000 * (-1.08631 + 1.0805))),  # -58
            ],
        },
    ]

    short_results = [i.to_dict() for i in short_operation_points]
    expected_short_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [
                -int(round(10000 * (-1.08448 + 1.08715))),  # -27
                -int(round(10000 * (-1.08448 + 1.08026))),  #  42
                -int(round(10000 * (-1.08448 + 1.08767))),  # -32
                -int(round(10000 * (-1.08448 + 1.0805))),  #  40
            ],
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": 32,
            "tp": 32,
            "sl": 16,
            "short_balance": [
                -int(round(10000 * (-1.08631 + 1.08767))),  # -14
                -int(round(10000 * (-1.08631 + 1.0805))),  #  58
            ],
        },
    ]

    assert (
        i.money_management_strategy_id == money_management_strategy.id
        for i in long_operation_points
    )
    assert (
        i.money_management_strategy_id == money_management_strategy.id
        for i in short_operation_points
    )
    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)
