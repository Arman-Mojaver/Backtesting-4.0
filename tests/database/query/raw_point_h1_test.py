import pytest

from database.models import RawPointD1, RawPointH1
from database.models.raw_point_h1 import MultipleValuesError
from testing_utils.dict_utils import (
    dicts_by_key_are_equal,
    dicts_multi_by_key_are_equal,
    lists_are_equal,
)


@pytest.fixture
def raw_point_d1(session):
    point_data = {
        "datetime": "2023-11-13",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point = RawPointD1(**point_data)

    session.add(point)
    session.commit()

    yield point

    session.delete(point)
    session.commit()


@pytest.fixture
def points(raw_point_d1, session):
    point_data_1 = {
        "datetime": "2023-11-13 00:00",
        "instrument": "EURUSD",
        "open": 1.06751,
        "high": 1.0706,
        "low": 1.06648,
        "close": 1.06981,
        "volume": 47554,
    }

    point_data_2 = {
        "datetime": "2023-11-13 01:00",
        "instrument": "EURUSD",
        "open": 1.06916,
        "high": 1.08872,
        "low": 1.06916,
        "close": 1.08782,
        "volume": 79728,
    }

    point_1 = RawPointH1(raw_point_d1_id=raw_point_d1.id, **point_data_1)
    point_2 = RawPointH1(raw_point_d1_id=raw_point_d1.id, **point_data_2)

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


def test_all(session, points):
    assert lists_are_equal(RawPointH1.query.all(), points)


def test_dict_by_key_default(session, points):
    point_1, point_2 = points

    result = RawPointH1.query.dict_by_key()
    expected_result = {
        point_1.id: point_1,
        point_2.id: point_2,
    }

    assert dicts_by_key_are_equal(result, expected_result)


def test_dict_by_key_with_key(session, points):
    point_1, point_2 = points

    result = RawPointH1.query.dict_by_key("datetime")
    expected_result = {
        point_1.datetime: point_1,
        point_2.datetime: point_2,
    }

    assert dicts_by_key_are_equal(result, expected_result)


@pytest.mark.usefixtures("points")
def test_dict_by_key_with_non_unique_key_raises_error(session):
    with pytest.raises(MultipleValuesError):
        RawPointH1.query.dict_by_key("instrument")


def test_dict_multi_by_key_with_multiple_items_per_key(session, points):
    point_1, point_2 = points

    result = RawPointH1.query.dict_multi_by_key("instrument")
    expected_result = {"EURUSD": [point_1, point_2]}

    assert dicts_multi_by_key_are_equal(result, expected_result)


def test_dict_multi_by_key_with_single_item_per_key(session, points):
    point_1, point_2 = points

    result = RawPointH1.query.dict_multi_by_key("id")
    expected_result = {
        point_1.id: [point_1],
        point_2.id: [point_2],
    }

    assert dicts_multi_by_key_are_equal(result, expected_result)
