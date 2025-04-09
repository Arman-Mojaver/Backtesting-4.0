from database.models import RawPointD1, RawPointH1
from testing_utils.dict_utils import lists_are_equal


def test_all_empty_raw_point_d1():
    assert lists_are_equal(RawPointD1.query.all(), [])


def test_all_raw_point_d1(other_raw_points):
    raw_point_d1, _ = other_raw_points
    assert lists_are_equal(RawPointD1.query.all(), [raw_point_d1])


def test_all_empty_raw_point_h1():
    assert lists_are_equal(RawPointH1.query.all(), [])


def test_all_raw_point_h1(other_raw_points):
    _, raw_points_h1 = other_raw_points
    assert lists_are_equal(RawPointH1.query.all(), raw_points_h1)
