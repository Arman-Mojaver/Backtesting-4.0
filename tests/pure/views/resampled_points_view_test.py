import pytest

from config import config  # type: ignore[attr-defined]
from database.models import RawPointD1, RawPointH1
from fixtures.price_data import get_points_data, get_resampled_d1_data
from utils.date_utils import datetime_to_string, string_to_datetime
from utils.enums import TimeFrame
from views.resampled_points_view import (
    NoRawPointsError,
    ResampledPointsCreateMultipleView,
)

# TODO: use more than one instrument in the tests  # noqa: TD002, TD003, FIX002


@pytest.fixture
def raw_points_d1():
    points_data = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-09-01"),
    )

    return [RawPointD1(**point_data) for point_data in points_data]


@pytest.fixture
def raw_points_d1_with_h1(raw_points_d1):
    points_data = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Hour,
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-09-01"),
    )

    raw_points_d1_by_date = {point.datetime: point for point in raw_points_d1}

    for point_data in points_data:
        date = datetime_to_string(
            string_to_datetime(point_data["datetime"], format=config.DATETIME_FORMAT)
        )

        raw_point_h1 = RawPointH1(**point_data)
        raw_point_d1 = raw_points_d1_by_date[date]
        raw_point_d1.raw_points_h1.append(raw_point_h1)

    return raw_points_d1


@pytest.fixture
def resampled_points_d1_data():
    return get_resampled_d1_data(
        instrument="EURUSD",
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-09-01"),
    )


def test_empty_raw_points_returns_error():
    with pytest.raises(NoRawPointsError):
        ResampledPointsCreateMultipleView([]).run()


def test_only_raw_points_d1_exist(raw_points_d1):
    with pytest.raises(NoRawPointsError):
        ResampledPointsCreateMultipleView(raw_points_d1).run()


def test_create_resampled_points(raw_points_d1_with_h1, resampled_points_d1_data):
    resampled_points = ResampledPointsCreateMultipleView(raw_points_d1_with_h1).run()

    assert [point.to_dict() for point in resampled_points] == resampled_points_d1_data
