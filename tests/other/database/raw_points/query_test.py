from database.models import RawPointD1, RawPointH1
from testing_utils.set_utils import set_of_tuples


def test_all_empty_raw_point_d1():
    assert RawPointD1.query.all() == []


def test_all_raw_point_d1(other_raw_points):
    raw_point_d1, _ = other_raw_points
    assert set_of_tuples(RawPointD1.query.all()) == set_of_tuples([raw_point_d1])


def test_all_empty_raw_point_h1():
    assert RawPointH1.query.all() == []


def test_all_raw_point_h1(other_raw_points):
    _, raw_points_h1 = other_raw_points
    assert set_of_tuples(RawPointH1.query.all()) == set_of_tuples(raw_points_h1)
