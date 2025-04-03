from testing_utils.finance_utils.global_roi import calculate_global_roi
from testing_utils.finance_utils.models import OperationItem


def test_negative_item():
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

    assert calculate_global_roi(operation_items) == round((cumsum - 1) * 100, 2)


def test_several_negative_items():
    operation_items = [
        OperationItem(
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
        OperationItem(
            result=-40,
            tp=30,
            sl=40,
            risk=0.02,
        ),
        OperationItem(
            result=-50,
            tp=30,
            sl=50,
            risk=0.02,
        ),
    ]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    cumsum += (-40) * (0.02 / 40)
    cumsum += (-50) * (0.02 / 50)

    assert calculate_global_roi(operation_items) == round((cumsum - 1) * 100, 2)


def test_positive_item():
    operation_items = [
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        )
    ]

    cumsum = 1
    cumsum += 30 * (0.02 / 20)

    assert calculate_global_roi(operation_items) == round((cumsum - 1) * 100, 2)


def test_several_positive_items():
    operation_items = [
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

    cumsum = 1
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)

    assert calculate_global_roi(operation_items) == round((cumsum - 1) * 100, 2)


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
        OperationItem(
            result=30,
            tp=30,
            sl=20,
            risk=0.02,
        ),
    ]

    cumsum = 1
    cumsum += (-20) * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)

    assert calculate_global_roi(operation_items) == round((cumsum - 1) * 100, 2)


def test_positive_and_negative_items():
    operation_items = [
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
            result=-20,
            tp=30,
            sl=20,
            risk=0.02,
        ),
    ]

    cumsum = 1
    cumsum += 30 * (0.02 / 20)
    cumsum += 30 * (0.02 / 20)
    cumsum += (-20) * (0.02 / 20)

    assert calculate_global_roi(operation_items) == round((cumsum - 1) * 100, 2)
