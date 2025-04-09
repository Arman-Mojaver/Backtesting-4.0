from __future__ import annotations

from testing_utils.finance_utils.draw_down import calculate_max_draw_down
from testing_utils.finance_utils.models import OperationItem

DRAW_DOWN_RESULT_MAPPING = {
    ((20, 20, 20),): 0,
    ((20, 20, 20), (30, 30, 20), (40, 40, 20)): 0,
    ((-20, 30, 20),): 2,
    ((-20, 30, 20), (-35, 30, 35), (-50, 30, 50)): 6.0,
    ((30, 30, 20), (-20, 30, 20)): 1.94,
    ((-20, 30, 20), (30, 30, 20)): 2.0,
    ((30, 30, 20), (-20, 30, 20), (-20, 30, 20)): 3.88,
    ((-20, 30, 20), (-20, 30, 20), (30, 30, 20), (30, 30, 20), (30, 30, 20)): 4.0,
    (
        (-20, 30, 20),
        (-20, 30, 20),
        (30, 30, 20),
        (25, 25, 20),
        (-200, 300, 200),
        (300, 300, 250),
    ): 4.0,
    (
        (-20, 30, 20),
        (-20, 30, 20),
        (30, 30, 20),
        (25, 25, 20),
        (-200, 300, 200),
        (-250, 300, 250),
        (-250, 300, 250),
    ): 5.91,
}


def test_only_positive_results_returns_zero_1():
    parameters = ((20, 20, 20),)
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

    assert calculate_max_draw_down(operation_items) == 0
    assert expected_result == 0


def test_only_positive_results_returns_zero_2():
    parameters = ((20, 20, 20), (30, 30, 20), (40, 40, 20))
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

    assert calculate_max_draw_down(operation_items) == 0
    assert expected_result == 0


def test_one_negative_result():
    parameters = ((-20, 30, 20),)
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)

    max_draw_down = round((1 - cumsum) / 1 * 100, 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down
    assert max_draw_down == expected_result


def test_three_negative_results():
    parameters = ((-20, 30, 20), (-35, 30, 35), (-50, 30, 50))
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    cumsum += (-35) * (0.02 / 35)
    cumsum += (-50) * (0.02 / 50)

    max_draw_down = round((1 - cumsum) / 1 * 100, 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down
    assert max_draw_down == expected_result


def test_positive_and_negative_items():
    parameters = ((30, 30, 20), (-20, 30, 20))
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

    cumsum = 1
    cumsum += 30 * (0.02 / 20)
    cummax = cumsum  # new max reached
    cumsum += (-20) * (0.02 / 20)

    max_draw_down = round((cummax - cumsum) / cummax * 100, 2)

    assert calculate_max_draw_down(operation_items) == max_draw_down
    assert max_draw_down == expected_result


def test_negative_and_positive_items():
    parameters = ((-20, 30, 20), (30, 30, 20))
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

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
    assert max_draw_down == expected_result


def test_positive_and_several_negative_items():
    parameters = ((30, 30, 20), (-20, 30, 20), (-20, 30, 20))
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

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
    assert max_draw_down == expected_result


def test_several_negative_and_several_positive_items():
    parameters = ((-20, 30, 20), (-20, 30, 20), (30, 30, 20), (30, 30, 20), (30, 30, 20))
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

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
    assert max_draw_down == expected_result


def test_mixed_order_of_positive_and_negative_items_1():
    parameters = (
        (-20, 30, 20),
        (-20, 30, 20),
        (30, 30, 20),
        (25, 25, 20),
        (-200, 300, 200),
        (300, 300, 250),
    )
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

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
    assert max_draw_down == expected_result


def test_mixed_order_of_positive_and_negative_items_2():
    parameters = (
        (-20, 30, 20),
        (-20, 30, 20),
        (30, 30, 20),
        (25, 25, 20),
        (-200, 300, 200),
        (-250, 300, 250),
        (-250, 300, 250),
    )
    expected_result = DRAW_DOWN_RESULT_MAPPING[parameters]
    operation_items = [OperationItem(*parameter, risk=0.02) for parameter in parameters]

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
    assert max_draw_down == expected_result
