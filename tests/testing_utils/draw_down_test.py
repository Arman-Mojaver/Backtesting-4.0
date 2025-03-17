from __future__ import annotations

import pytest

from testing_utils.draw_down import OperationItem, calculate_max_draw_down


@pytest.mark.parametrize(
    "operation_items",
    [
        [
            OperationItem(
                result=20,
                tp=20,
                sl=20,
                risk=0.02,
            )
        ],
        [
            OperationItem(
                result=20,
                tp=20,
                sl=20,
                risk=0.02,
            ),
            OperationItem(
                result=30,
                tp=30,
                sl=20,
                risk=0.02,
            ),
            OperationItem(
                result=40,
                tp=40,
                sl=20,
                risk=0.02,
            ),
        ],
    ]
)
def test_only_positive_results_returns_zero(operation_items):
    assert calculate_max_draw_down(operation_items) == 0


def test_one_negative_result():
    operation_items = [
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        )
    ]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)

    max_draw_down = round((1 - cumsum) / 1 * 100, 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down


def test_three_negative_results():
    operation_items = [
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-35,
            tp=30,
            sl=35,
            risk=0.02,
        ),
        OperationItem(
            result=-50,
            tp=30,
            sl=50,
            risk=0.02,
        )
    ]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    cumsum += (-35) * (0.02 / 35)
    cumsum += (-50) * (0.02 / 50)

    max_draw_down = round((1 - cumsum) / 1 * 100, 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down


def test_positive_and_negative_items():
    operation_items = [
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        )
    ]

    cumsum = 1
    cumsum += 30 * (0.02 / 20)
    cummax = cumsum  # new max reached
    cumsum += (-20) * (0.02 / 20)

    max_draw_down = round((cummax - cumsum) / cummax * 100, 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down


def test_negative_and_positive_items():
    operation_items = [
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
    ]

    cumsum_list, cummax_list = [], []

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(1)  # new max not reached

    cumsum += 30 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cumsum)  # new max reached

    draw_downs = [
        (cummax - cumsum) / cummax * 100
        for cumsum, cummax in zip(cumsum_list, cummax_list)
    ]

    max_draw_down = round(draw_downs[0], 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down


def test_positive_and_several_negative_items():
    operation_items = [
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        )
    ]

    cumsum_list, cummax_list = [], []
    cumsum = 1

    cumsum += 30 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cumsum)  # new max reached

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    draw_downs = [
        round((cummax - cumsum) / cummax * 100, 2)
        for cumsum, cummax in zip(cumsum_list, cummax_list)
    ]

    max_draw_down = round(draw_downs[2], 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down


def test_several_negative_and_several_positive_items():
    operation_items = [
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
    ]

    cumsum_list, cummax_list = [], []
    cumsum = 1

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(1)  # new max not reached

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += 30 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += 30 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cumsum)  # new max reached

    cumsum += 30 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cumsum)  # new max reached

    draw_downs = [
        round((cummax - cumsum) / cummax * 100, 2)
        for cumsum, cummax in zip(cumsum_list, cummax_list)
    ]

    max_draw_down = round(draw_downs[1], 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down


def test_mixed_order_of_positive_and_negative_items_1():
    operation_items = [
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=25,
            tp=25,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-200,
            tp=300,
            sl=200,
            risk=0.02,
        ),
        OperationItem(
            result=300,
            tp=300,
            sl=250,
            risk=0.02,
        ),
    ]

    cumsum_list, cummax_list = [], []
    cumsum = 1

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(1)  # new max not reached

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += 30 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += 25 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cumsum)  # new max reached

    cumsum += -200 * (0.02 / 200)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += 300 * (0.02 / 250)
    cumsum_list.append(cumsum)
    cummax_list.append(cumsum)  # new max reached

    draw_downs = [
        round((cummax - cumsum) / cummax * 100, 2)
        for cumsum, cummax in zip(cumsum_list, cummax_list)
    ]

    max_draw_down = round(draw_downs[1], 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down


def test_mixed_order_of_positive_and_negative_items_2():
    operation_items = [
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=25,
            tp=25,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-200,
            tp=300,
            sl=200,
            risk=0.02,
        ),
        OperationItem(
            result=-250,
            tp=300,
            sl=250,
            risk=0.02,
        ),
        OperationItem(
            result=-250,
            tp=300,
            sl=250,
            risk=0.02,
        ),
    ]

    cumsum_list, cummax_list = [], []
    cumsum = 1

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(1)  # new max not reached

    cumsum += -20 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += 30 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += 25 * (0.02 / 20)
    cumsum_list.append(cumsum)
    cummax_list.append(cumsum)  # new max reached

    cumsum += -200 * (0.02 / 200)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += -250 * (0.02 / 250)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    cumsum += -250 * (0.02 / 250)
    cumsum_list.append(cumsum)
    cummax_list.append(cummax_list[-1])  # new max not reached

    draw_downs = [
        round((cummax - cumsum) / cummax * 100, 2)
        for cumsum, cummax in zip(cumsum_list, cummax_list)
    ]

    max_draw_down = round(draw_downs[6], 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down
