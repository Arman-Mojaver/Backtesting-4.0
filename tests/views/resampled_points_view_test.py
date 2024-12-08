from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from config import config  # type: ignore[attr-defined]
from database.models import RawPointD1, RawPointH1, ResampledPointD1
from database.models.resasmpled_point_d1 import HighLowOrder
from fixtures.price_data import get_points_data
from utils.date_utils import datetime_to_string, string_to_datetime
from utils.enums import TimeFrame
from views.resampled_points_view import (
    NoRawPointsError,
    ResampledPointsCreateMultipleView,
)


@pytest.fixture
def raw_points_d1(session):
    points_data = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-09-01"),
    )

    points = []
    for point_data in points_data:
        point = RawPointD1(**point_data)
        points.append(point)

    session.add_all(points)
    session.commit()

    yield points

    for point in points:
        session.delete(point)

    session.commit()


@pytest.fixture
def raw_points_h1(raw_points_d1, session):
    points_data = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Hour,
        from_date=string_to_datetime("2023-08-21"),
        to_date=string_to_datetime("2023-09-01"),
    )

    raw_points_d1_by_date = {
        datetime_to_string(point.datetime): point for point in raw_points_d1
    }

    points = []
    for point_data in points_data:
        date = datetime_to_string(
            string_to_datetime(point_data["datetime"], format=config.DATETIME_FORMAT)
        )

        point = RawPointH1(
            raw_point_d1_id=raw_points_d1_by_date[date].id,
            **point_data,
        )
        points.append(point)

    session.add_all(points)
    session.commit()

    yield points

    for point in points:
        session.delete(point)

    session.commit()


def test_empty_raw_points_returns_error():
    with pytest.raises(NoRawPointsError):
        ResampledPointsCreateMultipleView().run()


@pytest.mark.usefixtures("raw_points_d1")
def test_only_raw_points_d1_exist():
    with pytest.raises(NoRawPointsError):
        ResampledPointsCreateMultipleView().run()


@pytest.fixture
def _clear_resampled_point_tables(session):
    yield
    session.query(ResampledPointD1).delete()
    session.commit()


@pytest.mark.usefixtures(
    "raw_points_d1",
    "raw_points_h1",
    "_clear_resampled_point_tables",
)
def test_create_resampled_points(session):
    ResampledPointsCreateMultipleView().run()

    resampled_points = ResampledPointD1.query.all()

    assert resampled_points[0].high_low_order == HighLowOrder.low_first
    assert resampled_points[1].high_low_order == HighLowOrder.high_first
    assert resampled_points[2].high_low_order == HighLowOrder.high_first
    assert resampled_points[3].high_low_order == HighLowOrder.high_first
    assert resampled_points[4].high_low_order == HighLowOrder.undefined
    assert resampled_points[5].high_low_order == HighLowOrder.low_first
    assert resampled_points[6].high_low_order == HighLowOrder.low_first
    assert resampled_points[7].high_low_order == HighLowOrder.low_first
    assert resampled_points[8].high_low_order == HighLowOrder.high_first
    assert resampled_points[9].high_low_order == HighLowOrder.undefined


@patch("views.resampled_points_view.session")
@pytest.mark.usefixtures(
    "raw_points_d1",
    "raw_points_h1",
    "_clear_resampled_point_tables",
)
def test_commit_error(mock_session):
    mock_session.commit.side_effect = SQLAlchemyError

    ResampledPointsCreateMultipleView().run()

    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
