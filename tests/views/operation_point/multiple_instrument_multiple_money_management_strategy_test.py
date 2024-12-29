from unittest.mock import patch

import pytest

from database.models import (
    LongOperationPoint,
    ShortOperationPoint,
)
from testing_utils.dict_utils import list_of_dicts_are_equal
from views.operation_points_view import OperationPointsCreateMultipleView


@patch("config.testing.TestingConfig.ENABLED_INSTRUMENTS", ("EURUSD", "USDCAD"))
@pytest.mark.usefixtures("three_resampled_points_d1_two_instruments")
def test_create(
    money_management_strategies,
    delete_operation_points,
    session,
):
    OperationPointsCreateMultipleView().run()

    money_management_strategy_1, money_management_strategy_2 = money_management_strategies

    # EURUSD

    long_operation_points_eurusd_1 = (
        session.query(LongOperationPoint)
        .filter_by(
            instrument="EURUSD",
            money_management_strategy_id=money_management_strategy_1.id,
        )
        .all()
    )
    long_operation_points_eurusd_2 = (
        session.query(LongOperationPoint)
        .filter_by(
            instrument="EURUSD",
            money_management_strategy_id=money_management_strategy_2.id,
        )
        .all()
    )
    short_operation_points_eurusd_1 = (
        session.query(ShortOperationPoint)
        .filter_by(
            instrument="EURUSD",
            money_management_strategy_id=money_management_strategy_1.id,
        )
        .all()
    )

    short_operation_points_eurusd_2 = (
        session.query(ShortOperationPoint)
        .filter_by(
            instrument="EURUSD",
            money_management_strategy_id=money_management_strategy_2.id,
        )
        .all()
    )

    # money_management_strategy_1

    long_results_eurusd_1 = [i.to_dict() for i in long_operation_points_eurusd_1]
    expected_long_results_eurusd_1 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42],
        }
    ]

    short_results_eurusd_1 = [i.to_dict() for i in short_operation_points_eurusd_1]
    expected_short_results_eurusd_1 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [-27],  # [-27, 42]
        }
    ]

    # money_management_strategy_2

    long_results_eurusd_2 = [i.to_dict() for i in long_operation_points_eurusd_2]
    expected_long_results_eurusd_2 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -22,
            "tp": 43,
            "sl": 22,
            "long_balance": [27, -42],
        }
    ]

    short_results_eurusd_2 = [i.to_dict() for i in short_operation_points_eurusd_2]
    expected_short_results_eurusd_2 = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -22,
            "tp": 43,
            "sl": 22,
            "short_balance": [-27],  # [-27, 42]
        }
    ]

    assert (
        i.money_management_strategy_id == money_management_strategy_1.id
        for i in long_operation_points_eurusd_1 + short_operation_points_eurusd_1
    )
    assert (
        i.money_management_strategy_id == money_management_strategy_2.id
        for i in long_operation_points_eurusd_2 + short_operation_points_eurusd_2
    )
    assert list_of_dicts_are_equal(long_results_eurusd_1, expected_long_results_eurusd_1)
    assert list_of_dicts_are_equal(
        short_results_eurusd_1, expected_short_results_eurusd_1
    )
    assert list_of_dicts_are_equal(long_results_eurusd_2, expected_long_results_eurusd_2)
    assert list_of_dicts_are_equal(
        short_results_eurusd_2, expected_short_results_eurusd_2
    )

    # USDCAD

    long_operation_points_usdcad_1 = (
        session.query(LongOperationPoint)
        .filter_by(
            instrument="USDCAD",
            money_management_strategy_id=money_management_strategy_1.id,
        )
        .all()
    )
    long_operation_points_usdcad_2 = (
        session.query(LongOperationPoint)
        .filter_by(
            instrument="USDCAD",
            money_management_strategy_id=money_management_strategy_2.id,
        )
        .all()
    )
    short_operation_points_usdcad_1 = (
        session.query(ShortOperationPoint)
        .filter_by(
            instrument="USDCAD",
            money_management_strategy_id=money_management_strategy_1.id,
        )
        .all()
    )

    short_operation_points_usdcad_2 = (
        session.query(ShortOperationPoint)
        .filter_by(
            instrument="USDCAD",
            money_management_strategy_id=money_management_strategy_2.id,
        )
        .all()
    )

    # money_management_strategy_1

    long_results_usdcad_1 = [i.to_dict() for i in long_operation_points_usdcad_1]

    expected_long_results_usdcad_1 = [
        {
            "instrument": "USDCAD",
            "datetime": "2023-11-15",
            "result": -18,
            "tp": 36,
            "sl": 18,
            "long_balance": [26, -29],
        }
    ]

    short_results_usdcad_1 = [i.to_dict() for i in short_operation_points_usdcad_1]
    expected_short_results_usdcad_1 = [
        {
            "instrument": "USDCAD",
            "datetime": "2023-11-15",
            "result": -18,
            "tp": 36,
            "sl": 18,
            "short_balance": [-26],  # [-26, 29]
        }
    ]

    # money_management_strategy_2

    long_results_usdcad_2 = [i.to_dict() for i in long_operation_points_usdcad_2]
    short_results_usdcad_2 = [i.to_dict() for i in short_operation_points_usdcad_2]

    assert (
        i.money_management_strategy_id == money_management_strategy_1.id
        for i in long_operation_points_usdcad_1 + short_operation_points_usdcad_1
    )
    assert (
        i.money_management_strategy_id == money_management_strategy_2.id
        for i in long_operation_points_usdcad_2 + short_operation_points_usdcad_2
    )
    assert list_of_dicts_are_equal(long_results_usdcad_1, expected_long_results_usdcad_1)
    assert list_of_dicts_are_equal(
        short_results_usdcad_1, expected_short_results_usdcad_1
    )
    assert long_results_usdcad_2 == []
    assert short_results_usdcad_2 == []
