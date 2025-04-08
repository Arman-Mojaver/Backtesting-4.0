import pytest

from database.models import RawPointD1, RawPointH1
from views.raw_points.raw_points_view import RawPointsCreateMultipleView


@pytest.fixture(autouse=True)
def _clear_raw_point_tables(session):
    yield
    for point in session.query(RawPointH1).all():
        session.delete(point)
    session.commit()


def test_create_raw_points(file_data):
    raw_points_d1 = RawPointsCreateMultipleView(file_data, ("EURUSD", "USDCAD")).run()
    raw_points_h1 = [
        point for raw_point_d1 in raw_points_d1 for point in raw_point_d1.raw_points_h1
    ]

    expected_raw_points_d1 = [
        RawPointD1(**point_data)
        for instrument in file_data["data"].values()
        for point_data in instrument["raw_points_d1"]
    ]
    expected_raw_points_h1 = [
        RawPointH1(**point_data)
        for instrument in file_data["data"].values()
        for point_data in instrument["raw_points_h1"]
    ]

    assert {p.to_tuple() for p in raw_points_d1} == {
        p.to_tuple() for p in expected_raw_points_d1
    }
    assert {p.to_tuple() for p in raw_points_h1} == {
        p.to_tuple() for p in expected_raw_points_h1
    }
