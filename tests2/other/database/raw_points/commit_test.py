import pytest
from sqlalchemy.exc import IntegrityError

from database.handler import DatabaseHandler
from database.models import RawPointD1, RawPointH1
from testing_utils.dict_utils import lists_are_equal


def test_commit_success_multiple_with_empty_tables(  # noqa: PLR0913
    raw_point_d1_data_1,
    raw_point_d1_data_2,
    raw_points_h1_data_1,
    raw_points_h1_data_2,
    raw_points,
    session,
):
    DatabaseHandler(session).commit_raw_points(raw_points)

    raw_point_d1_1 = RawPointD1(**raw_point_d1_data_1)
    raw_points_h1_1 = [
        RawPointH1(**raw_point_h1_data) for raw_point_h1_data in raw_points_h1_data_1
    ]
    raw_point_d1_2 = RawPointD1(**raw_point_d1_data_2)
    raw_points_h1_2 = [
        RawPointH1(**raw_point_h1_data) for raw_point_h1_data in raw_points_h1_data_2
    ]

    assert lists_are_equal(
        session.query(RawPointD1).all(),
        [raw_point_d1_1, raw_point_d1_2],
    )
    assert lists_are_equal(
        session.query(RawPointH1).all(),
        [*raw_points_h1_1, *raw_points_h1_2],
    )


def test_commit_success_multiple_with_existing_tables_items(  # noqa: PLR0913
    other_raw_points,
    raw_point_d1_data_1,
    raw_point_d1_data_2,
    raw_points_h1_data_1,
    raw_points_h1_data_2,
    raw_points,
    session,
):
    raw_point_d1, raw_points_h1 = other_raw_points

    DatabaseHandler(session).commit_raw_points(raw_points)

    raw_point_d1_1 = RawPointD1(**raw_point_d1_data_1)
    raw_points_h1_1 = [
        RawPointH1(**raw_point_h1_data) for raw_point_h1_data in raw_points_h1_data_1
    ]
    raw_point_d1_2 = RawPointD1(**raw_point_d1_data_2)
    raw_points_h1_2 = [
        RawPointH1(**raw_point_h1_data) for raw_point_h1_data in raw_points_h1_data_2
    ]

    assert lists_are_equal(
        session.query(RawPointD1).all(),
        [raw_point_d1_1, raw_point_d1_2, raw_point_d1],
    )
    assert lists_are_equal(
        session.query(RawPointH1).all(),
        [*raw_points_h1_1, *raw_points_h1_2, *raw_points_h1],
    )


def test_commit_raw_point_d1_with_colliding_identifiers_raises_error(
    other_raw_points,
    session,
):
    raw_point_d1, _ = other_raw_points
    repeated_item = RawPointD1(**raw_point_d1.to_dict())

    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_raw_points([repeated_item])


def test_commit_raw_point_h1_with_colliding_identifiers_raises_error(
    other_raw_points,
    session,
):
    raw_point_d1, raw_points_h1 = other_raw_points
    repeated_item = RawPointH1(**raw_points_h1[0].to_dict())
    raw_point_d1.raw_points_h1.append(repeated_item)

    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_raw_points([raw_point_d1])
