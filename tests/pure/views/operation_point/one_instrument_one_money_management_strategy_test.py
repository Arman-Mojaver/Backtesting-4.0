import pytest

from database.models import MoneyManagementStrategy
from fixtures.helpers import generate_identifier
from testing_utils.dict_utils import list_of_dicts_are_equal
from views.operation_points_view import OperationPointsCreateMultipleView


def test_create_one_pair_without_balance_overflow(
    three_resampled_points_d1,
    money_management_strategy,
):
    operation_points = OperationPointsCreateMultipleView(
        three_resampled_points_d1,
        [money_management_strategy],
        enabled_instruments=("EURUSD",),
    ).run()

    long_operation_points = operation_points.long_operation_points
    short_operation_points = operation_points.short_operation_points

    atr = int(
        round(
            10000
            * (
                sum(
                    [
                        1.09137 - 1.08634,
                        max(
                            abs(1.09305 - 1.08329),
                            abs(1.09305 - 1.08949),
                            abs(1.08329 - 1.08949),
                        ),
                        max(
                            abs(1.08715 - 1.08026),
                            abs(1.08715 - 1.08452),
                            abs(1.08026 - 1.08452),
                        ),
                    ]
                )
                / 3
            )
        )
    )

    tp = round(money_management_strategy.tp_multiplier * atr)
    sl = round(money_management_strategy.sl_multiplier * atr)

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -sl,  # -14
            "tp": tp,  # 29
            "sl": sl,  # 14
            "long_balance": [
                int(round(10000 * (-1.08448 + 1.08715))),  # 27
                int(round(10000 * (-1.08448 + 1.08026))),  # -42
            ],
            "risk": 0.02,
        }
    ]

    short_results = [i.to_dict() for i in short_operation_points]
    expected_short_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -sl,  # -14
            "tp": tp,  # 29
            "sl": sl,  # 14
            "short_balance": [-int(round(10000 * (-1.08448 + 1.08715)))],  # -27
            "risk": 0.02,
        }
    ]

    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)


def test_create_two_pairs_without_balance_overflow(
    money_management_strategy,
    four_resampled_points_d1,
):
    operation_points = OperationPointsCreateMultipleView(
        four_resampled_points_d1,
        [money_management_strategy],
        enabled_instruments=("EURUSD",),
    ).run()

    long_operation_points = operation_points.long_operation_points
    short_operation_points = operation_points.short_operation_points

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42],  # [27, -42, 32, -40]
            "risk": 0.02,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -16,
            "tp": 32,
            "sl": 16,
            "long_balance": [14, -58],
            "risk": 0.02,
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
            "short_balance": [-27],  # [-27, 42, -32, 40]
            "risk": 0.02,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": 32,
            "tp": 32,
            "sl": 16,
            "short_balance": [-14, 58],
            "risk": 0.02,
        },
    ]

    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)


@pytest.fixture
def money_management_strategy_with_large_multipliers():
    money_management_strategy_data = {
        "type": "atr",
        "tp_multiplier": 500,
        "sl_multiplier": 500,
        "parameters": {"atr_parameter": 3},
        "risk": 0.02,
    }

    return MoneyManagementStrategy(
        **money_management_strategy_data,
        identifier=generate_identifier(money_management_strategy_data),
    )


def test_do_not_create_with_balance_overflow(
    money_management_strategy_with_large_multipliers,
    four_resampled_points_d1,
):
    operation_points = OperationPointsCreateMultipleView(
        four_resampled_points_d1,
        [money_management_strategy_with_large_multipliers],
        enabled_instruments=("EURUSD",),
    ).run()

    assert operation_points.long_operation_points == []
    assert operation_points.short_operation_points == []


@pytest.fixture
def money_management_strategy_with_symmetric_balance_overflow():
    money_management_strategy_data = {
        "type": "atr",
        "tp_multiplier": 0.4,
        "sl_multiplier": 0.2,
        "parameters": {"atr_parameter": 3},
        "risk": 0.02,
    }

    return MoneyManagementStrategy(
        **money_management_strategy_data,
        identifier=generate_identifier(money_management_strategy_data),
    )


def test_create_with_symmetric_balance_overflow(
    money_management_strategy_with_symmetric_balance_overflow,
    four_resampled_points_d1_low_atr,
):
    operation_points = OperationPointsCreateMultipleView(
        four_resampled_points_d1_low_atr,
        [money_management_strategy_with_symmetric_balance_overflow],
        enabled_instruments=("EURUSD",),
    ).run()

    long_operation_points = operation_points.long_operation_points
    short_operation_points = operation_points.short_operation_points

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42],  # [27, -42, 23, 13]
            "risk": 0.02,
        }
    ]

    short_results = [i.to_dict() for i in short_operation_points]
    expected_short_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "short_balance": [-27],  # [-27, 42, -23, -13]
            "risk": 0.02,
        }
    ]

    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)


def test_create_with_long_asymmetric_balance_overflow(
    money_management_strategy_with_symmetric_balance_overflow,
    five_resampled_points_d1_long_asymmetric_overflow,
):
    operation_points = OperationPointsCreateMultipleView(
        five_resampled_points_d1_long_asymmetric_overflow,
        [money_management_strategy_with_symmetric_balance_overflow],
        enabled_instruments=("EURUSD",),
    ).run()

    long_operation_points = operation_points.long_operation_points
    short_operation_points = operation_points.short_operation_points

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42],  # [27, -42, 32, -40, -15, -45]
            "risk": 0.02,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -16,
            "tp": 32,
            "sl": 16,
            "long_balance": [14, -58],  # [14, -58, -34, -64]
            "risk": 0.02,
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
            "short_balance": [-27],  # [-27, 42, -32, 40, 15, 45]
            "risk": 0.02,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": 32,
            "tp": 32,
            "sl": 16,
            "short_balance": [-14, 58],  # [-14, 58, 34, 64]
            "risk": 0.02,
        },
    ]

    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)


def test_create_with_short_asymmetric_balance_overflow(
    money_management_strategy_with_symmetric_balance_overflow,
    five_resampled_points_d1_short_asymmetric_overflow,
):
    operation_points = OperationPointsCreateMultipleView(
        five_resampled_points_d1_short_asymmetric_overflow,
        [money_management_strategy_with_symmetric_balance_overflow],
        enabled_instruments=("EURUSD",),
    ).run()

    long_operation_points = operation_points.long_operation_points
    short_operation_points = operation_points.short_operation_points

    long_results = [i.to_dict() for i in long_operation_points]
    expected_long_results = [
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-23",
            "result": -14,
            "tp": 29,
            "sl": 14,
            "long_balance": [27, -42],  # [27, -42, 32, -40, -55, -25]
            "risk": 0.02,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": -16,
            "tp": 32,
            "sl": 16,
            "long_balance": [14, -58],  # [14, -58, -74, -44]
            "risk": 0.02,
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
            "short_balance": [-27],  # [-27, 42, -32, 40, 55, 25]
            "risk": 0.02,
        },
        {
            "instrument": "EURUSD",
            "datetime": "2023-08-24",
            "result": 32,
            "tp": 32,
            "sl": 16,
            "short_balance": [-14, 58],  # [-14, 58, 74, 44]
            "risk": 0.02,
        },
    ]

    assert list_of_dicts_are_equal(long_results, expected_long_results)
    assert list_of_dicts_are_equal(short_results, expected_short_results)
