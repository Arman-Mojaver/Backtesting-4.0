import pytest

from database.models import RawPointD1, RawPointH1
from fixtures.price_data import get_points_data
from utils.date_utils import string_to_datetime
from utils.enums import TimeFrame


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    for item in session.query(RawPointD1).all():
        session.delete(item)
    session.commit()


@pytest.fixture
def raw_point_d1_data_1():
    return get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-13"),
    )[0]

@pytest.fixture
def raw_point_d1_data_2():
    return get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-11-14"),
        to_date=string_to_datetime("2023-11-14"),
    )[0]


@pytest.fixture
def raw_points_h1_data_1():
    return get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Hour,
        from_date=string_to_datetime("2023-11-13"),
        to_date=string_to_datetime("2023-11-13"),
    )

@pytest.fixture
def raw_points_h1_data_2():
    return get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Hour,
        from_date=string_to_datetime("2023-11-14"),
        to_date=string_to_datetime("2023-11-14"),
    )


@pytest.fixture
def raw_points(
    raw_point_d1_data_1,
    raw_point_d1_data_2,
    raw_points_h1_data_1,
    raw_points_h1_data_2,
):
    raw_point_d1_1 = RawPointD1(**raw_point_d1_data_1)
    raw_points_h1_1 = [
        RawPointH1(**raw_point_h1_data) for raw_point_h1_data in raw_points_h1_data_1
    ]
    raw_point_d1_2 = RawPointD1(**raw_point_d1_data_2)
    raw_points_h1_2 = [
        RawPointH1(**raw_point_h1_data) for raw_point_h1_data in raw_points_h1_data_2
    ]

    raw_point_d1_1.raw_points_h1 = raw_points_h1_1
    raw_point_d1_2.raw_points_h1 = raw_points_h1_2

    return [raw_point_d1_1, raw_point_d1_2]


@pytest.fixture
def other_raw_points(session):
    raw_point_d1_data = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Day,
        from_date=string_to_datetime("2023-11-15"),
        to_date=string_to_datetime("2023-11-15"),
    )[0]

    all_raw_point_h1_data = get_points_data(
        instrument="EURUSD",
        time_frame=TimeFrame.Hour,
        from_date=string_to_datetime("2023-11-15"),
        to_date=string_to_datetime("2023-11-16"),
    )

    raw_point_d1 = RawPointD1(**raw_point_d1_data)
    raw_points_h1 = [
        RawPointH1(**raw_point_h1_data) for raw_point_h1_data in all_raw_point_h1_data
    ]

    raw_point_d1.raw_points_h1 = raw_points_h1

    session.add(raw_point_d1)
    session.commit()

    return raw_point_d1, raw_points_h1
