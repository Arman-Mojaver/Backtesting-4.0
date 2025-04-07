from testing_utils.dict_utils import list_of_dicts_are_equal
from views.operation_points_view import OperationPointsCreateMultipleView


def test_create_one_pair_without_balance_overflow(
    money_management_strategies,
    three_resampled_points_d1,
):
    operation_points = OperationPointsCreateMultipleView(
        three_resampled_points_d1,
        money_management_strategies,
        enabled_instruments=("EURUSD",),
    ).run()

    long_operation_points = operation_points.long_operation_points
    short_operation_points = operation_points.short_operation_points

    money_management_strategy_1, money_management_strategy_2 = money_management_strategies

    long_operation_points_1 = [
        item
        for item in long_operation_points
        if item.money_management_strategy_id == money_management_strategy_1.id
    ]

    long_operation_points_2 = [
        item
        for item in long_operation_points
        if item.money_management_strategy_id == money_management_strategy_2.id
    ]

    short_operation_points_1 = [
        item
        for item in short_operation_points
        if item.money_management_strategy_id == money_management_strategy_1.id
    ]

    short_operation_points_2 = [
        item
        for item in short_operation_points
        if item.money_management_strategy_id == money_management_strategy_2.id
    ]

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
            "risk": 0.02,
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
            "short_balance": [-27],  # [-27, 42]
            "risk": 0.02,
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
            "risk": 0.02,
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
            "short_balance": [-27],  # [-27, 42]
            "risk": 0.02,
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
