from testing_utils.finance_utils.global_roi import calculate_global_roi
from testing_utils.finance_utils.models import OperationItem

ROI_RESULT_MAPPING = {
    ((-20, 30, 20),): -2.0,
    ((-20, 30, 20), (-40, 30, 40), (-50, 30, 50)): -6.0,
    ((30, 30, 20),): 3.0,
    ((30, 30, 20), (30, 30, 20), (30, 30, 20)): 9.0,
    ((-20, 30, 20), (30, 30, 20), (30, 30, 20)): 4.0,
    ((30, 30, 20), (30, 30, 20), (-20, 30, 20)): 4.0,
}


def test_negative_item():
    parameters = ((-20, 30, 20),)
    expected_result = ROI_RESULT_MAPPING[parameters]
    operation_items = [
        OperationItem(result, tp, sl, risk=0.02) for result, tp, sl in parameters
    ]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    roi = round((cumsum - 1) * 100, 2)

    assert calculate_global_roi(operation_items) == expected_result
    assert expected_result == roi


def test_several_negative_items():
    parameters = ((-20, 30, 20), (-40, 30, 40), (-50, 30, 50))
    expected_result = ROI_RESULT_MAPPING[parameters]
    operation_items = [
        OperationItem(result, tp, sl, risk=0.02) for result, tp, sl in parameters
    ]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    cumsum += (-40) * (0.02 / 40)
    cumsum += (-50) * (0.02 / 50)
    roi = round((cumsum - 1) * 100, 2)

    assert calculate_global_roi(operation_items) == expected_result
    assert expected_result == roi


def test_positive_item():
    parameters = ((30, 30, 20),)
    expected_result = ROI_RESULT_MAPPING[parameters]
    operation_items = [
        OperationItem(result, tp, sl, risk=0.02) for result, tp, sl in parameters
    ]

    cumsum = 1
    cumsum += 30 * (0.02 / 20)
    roi = round((cumsum - 1) * 100, 2)

    assert calculate_global_roi(operation_items) == expected_result
    assert expected_result == roi


def test_several_positive_items():
    parameters = ((30, 30, 20), (30, 30, 20), (30, 30, 20))
    expected_result = ROI_RESULT_MAPPING[parameters]
    operation_items = [
        OperationItem(result, tp, sl, risk=0.02) for result, tp, sl in parameters
    ]

    cumsum = 1
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    roi = round((cumsum - 1) * 100, 2)

    assert calculate_global_roi(operation_items) == expected_result
    assert expected_result == roi


def test_negative_and_positive_items():
    parameters = ((-20, 30, 20), (30, 30, 20), (30, 30, 20))
    expected_result = ROI_RESULT_MAPPING[parameters]
    operation_items = [
        OperationItem(result, tp, sl, risk=0.02) for result, tp, sl in parameters
    ]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    roi = round((cumsum - 1) * 100, 2)

    assert calculate_global_roi(operation_items) == expected_result
    assert expected_result == roi


def test_positive_and_negative_items():
    parameters = ((30, 30, 20), (30, 30, 20), (-20, 30, 20))
    expected_result = ROI_RESULT_MAPPING[parameters]
    operation_items = [
        OperationItem(result, tp, sl, risk=0.02) for result, tp, sl in parameters
    ]

    cumsum = 1
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    cumsum += (-20) * (0.02 / 20)
    roi = round((cumsum - 1) * 100, 2)

    assert calculate_global_roi(operation_items) == expected_result
    assert expected_result == roi
