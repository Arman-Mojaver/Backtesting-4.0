from database.models import ResampledPointD1
from testing_utils.dict_utils import lists_are_equal


def test_all_empty():
    assert lists_are_equal(ResampledPointD1.query.all(), [])


def test_all(other_resampled_points):
    assert lists_are_equal(ResampledPointD1.query.all(), other_resampled_points)
