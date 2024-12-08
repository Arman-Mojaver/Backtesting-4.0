import pytest

from database.models import RawPointD1
from database.models.raw_point_d1 import MultipleValuesError
from fixtures.price_data import get_points_data
from testing_utils.dict_utils import (
    dicts_by_key_are_equal,
    dicts_multi_by_key_are_equal,
    lists_are_equal,
)
from utils.date_utils import string_to_datetime
from utils.enums import TimeFrame


@pytest.fixture
def points(session):
    point_data_1, point_data_2 = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-14"),
    )

    point_1 = RawPointD1(**point_data_1)
    point_2 = RawPointD1(**point_data_2)

    session.add_all([point_1, point_2])
    session.commit()

    yield [point_1, point_2]

    session.delete(point_1)
    session.delete(point_2)
    session.commit()


def test_all(session, points):
    assert lists_are_equal(RawPointD1.query.all(), points)


def test_dict_by_key_default(session, points):
    point_1, point_2 = points

    result = RawPointD1.query.dict_by_key()
    expected_result = {
        point_1.id: point_1,
        point_2.id: point_2,
    }

    assert dicts_by_key_are_equal(result, expected_result)


def test_dict_by_key_with_key(session, points):
    point_1, point_2 = points

    result = RawPointD1.query.dict_by_key("datetime")
    expected_result = {
        point_1.datetime: point_1,
        point_2.datetime: point_2,
    }

    assert dicts_by_key_are_equal(result, expected_result)


@pytest.mark.usefixtures("points")
def test_dict_by_key_with_non_unique_key_raises_error(session):
    with pytest.raises(MultipleValuesError):
        RawPointD1.query.dict_by_key("instrument")


def test_dict_multi_by_key_with_multiple_items_per_key(session, points):
    point_1, point_2 = points

    result = RawPointD1.query.dict_multi_by_key("instrument")
    expected_result = {"EURUSD": [point_1, point_2]}

    assert dicts_multi_by_key_are_equal(result, expected_result)


def test_dict_multi_by_key_with_single_item_per_key(session, points):
    point_1, point_2 = points

    result = RawPointD1.query.dict_multi_by_key("id")
    expected_result = {
        point_1.id: [point_1],
        point_2.id: [point_2],
    }

    assert dicts_multi_by_key_are_equal(result, expected_result)
