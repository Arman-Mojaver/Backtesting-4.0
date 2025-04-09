import pytest
from sqlalchemy.exc import IntegrityError

from database.handler import DatabaseHandler
from database.models import ResampledPointD1
from testing_utils.dict_utils import lists_are_equal


def test_commit_success_multiple_with_empty_table(resampled_points, session):
    DatabaseHandler(session).commit_resampled_points(resampled_points)

    assert lists_are_equal(session.query(ResampledPointD1).all(), resampled_points)


def test_commit_success_multiple_with_existing_table(
    resampled_points,
    other_resampled_points,
    session,
):
    DatabaseHandler(session).commit_resampled_points(resampled_points)

    assert lists_are_equal(
        session.query(ResampledPointD1).all(),
        [*resampled_points, *other_resampled_points],
    )


def test_commit_resampled_point_with_colliding_identifiers_raises_error(
    other_resampled_points,
    session,
):
    point_data = other_resampled_points[0].to_dict()
    repeated_point = ResampledPointD1(**point_data)

    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_resampled_points([repeated_point])
