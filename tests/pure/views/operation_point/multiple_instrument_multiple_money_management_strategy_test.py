from testing_utils.dict_utils import list_of_dicts_are_equal
from utils.date_utils import string_to_datetime
from views.operation_points_view import OperationPointsCreateMultipleView


def test_create(
    money_management_strategies,
    three_resampled_points_d1_two_instruments,
):
    operation_points = OperationPointsCreateMultipleView(
        three_resampled_points_d1_two_instruments,
        money_management_strategies,
        enabled_instruments=("EURUSD", "USDCAD"),
    ).run()

    long_operation_points = operation_points.long_operation_points
    short_operation_points = operation_points.short_operation_points

    money_management_strategy_1, money_management_strategy_2 = money_management_strategies

    # EURUSD

    long_operation_points_eurusd_1 = [
        item
        for item in long_operation_points
        if item.money_management_strategy_id == money_management_strategy_1.id
        and item.instrument == "EURUSD"
    ]

    long_operation_points_eurusd_2 = [
        item
        for item in long_operation_points
        if item.money_management_strategy_id == money_management_strategy_2.id
        and item.instrument == "EURUSD"
    ]
    short_operation_points_eurusd_1 = [
        item
        for item in short_operation_points
        if item.money_management_strategy_id == money_management_strategy_1.id
        and item.instrument == "EURUSD"
    ]

    short_operation_points_eurusd_2 = [
        item
        for item in short_operation_points
        if item.money_management_strategy_id == money_management_strategy_2.id
        and item.instrument == "EURUSD"
    ]

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
            "risk": 0.02,
            "timestamp": int(string_to_datetime("2023-08-23").timestamp()),
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
            "risk": 0.02,
            "timestamp": int(string_to_datetime("2023-08-23").timestamp()),
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
            "risk": 0.02,
            "timestamp": int(string_to_datetime("2023-08-23").timestamp()),
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
            "risk": 0.02,
            "timestamp": int(string_to_datetime("2023-08-23").timestamp()),
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

    long_operation_points_usdcad_1 = [
        item
        for item in long_operation_points
        if item.money_management_strategy_id == money_management_strategy_1.id
        and item.instrument == "USDCAD"
    ]

    long_operation_points_usdcad_2 = [
        item
        for item in long_operation_points
        if item.money_management_strategy_id == money_management_strategy_2.id
        and item.instrument == "USDCAD"
    ]
    short_operation_points_usdcad_1 = [
        item
        for item in short_operation_points
        if item.money_management_strategy_id == money_management_strategy_1.id
        and item.instrument == "USDCAD"
    ]

    short_operation_points_usdcad_2 = [
        item
        for item in short_operation_points
        if item.money_management_strategy_id == money_management_strategy_2.id
        and item.instrument == "USDCAD"
    ]

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
            "risk": 0.02,
            "timestamp": int(string_to_datetime("2023-11-15").timestamp()),
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
            "risk": 0.02,
            "timestamp": int(string_to_datetime("2023-11-15").timestamp()),
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
