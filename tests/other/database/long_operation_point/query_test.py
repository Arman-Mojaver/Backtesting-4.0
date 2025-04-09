from database.models import LongOperationPoint
from testing_utils.dict_utils import lists_are_equal


def test_all_empty():
    assert lists_are_equal(LongOperationPoint.query.all(), [])


def test_all(long_operation_points):
    assert lists_are_equal(LongOperationPoint.query.all(), long_operation_points)
