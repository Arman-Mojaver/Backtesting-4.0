from database.models import ShortOperationPoint
from testing_utils.dict_utils import lists_are_equal


def test_all_empty():
    assert lists_are_equal(ShortOperationPoint.query.all(), [])


def test_all(short_operation_points):
    assert lists_are_equal(ShortOperationPoint.query.all(), short_operation_points)
