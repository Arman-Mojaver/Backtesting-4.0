from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from database.models import RawPointD1, RawPointH1
from testing_utils.dict_utils import list_of_dicts_are_equal
from views.raw_points.raw_points_view import RawPointsCreateMultipleView


@pytest.fixture
def _clear_raw_point_tables(session):
    yield
    session.query(RawPointH1).delete()
    session.query(RawPointD1).delete()
    session.commit()


@pytest.mark.usefixtures("_clear_raw_point_tables")
def test_create_raw_points(file_data):
    RawPointsCreateMultipleView(file_data, ("EURUSD", "USDCAD")).run()

    raw_points_d1 = RawPointD1.query.all()
    expected_raw_point_d1_data = [
        point_data
        for instrument in file_data["data"].values()
        for point_data in instrument["raw_points_d1"]
    ]

    raw_points_h1 = RawPointH1.query.all()
    expected_raw_point_h1_data = [
        point_data
        for instrument in file_data["data"].values()
        for point_data in instrument["raw_points_h1"]
    ]

    assert list_of_dicts_are_equal(
        [point.to_dict() for point in raw_points_d1],
        expected_raw_point_d1_data,
    )
    assert list_of_dicts_are_equal(
        [point.to_dict() for point in raw_points_h1],
        expected_raw_point_h1_data,
    )

    for point in RawPointH1.query.all():
        assert point.instrument == point.raw_point_d1.instrument


@patch("views.raw_points.raw_points_view.session")
def test_commit_error(mock_session, file_data):
    mock_session.commit.side_effect = SQLAlchemyError

    with pytest.raises(SQLAlchemyError):
        RawPointsCreateMultipleView(file_data, ("EURUSD", "USDCAD")).run()
