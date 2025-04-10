from database.models import LongOperationPoint
from testing_utils.set_utils import set_of_tuples


def test_all_empty():
    assert LongOperationPoint.query.all() == []


def test_all(other_long_operation_points):
    assert set_of_tuples(LongOperationPoint.query.all()) == set_of_tuples(
        other_long_operation_points
    )
