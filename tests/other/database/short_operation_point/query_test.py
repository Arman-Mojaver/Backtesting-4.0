from database.models import ShortOperationPoint
from testing_utils.set_utils import set_of_tuples


def test_all_empty():
    assert ShortOperationPoint.query.all() == []


def test_all(other_short_operation_points):
    assert set_of_tuples(ShortOperationPoint.query.all()) == set_of_tuples(
        other_short_operation_points
    )
