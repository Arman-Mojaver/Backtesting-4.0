import pytest
from sqlalchemy.exc import IntegrityError

from database.handler import DatabaseHandler
from database.models import LongOperationPoint, ShortOperationPoint
from models.operation_point import OperationPoints
from testing_utils.dict_utils import lists_are_equal


def test_commit_success_multiple_with_empty_table(
    long_operation_points,
    short_operation_points,
    session,
):
    operation_points = OperationPoints(long_operation_points, short_operation_points)
    DatabaseHandler(session).commit_operation_points(operation_points)

    assert lists_are_equal(session.query(LongOperationPoint).all(), long_operation_points)
    assert lists_are_equal(
        session.query(ShortOperationPoint).all(), short_operation_points
    )


def test_commit_success_multiple_with_existing_tables_items(
    other_long_operation_points,
    other_short_operation_points,
    long_operation_points,
    short_operation_points,
    session,
):
    operation_points = OperationPoints(long_operation_points, short_operation_points)
    DatabaseHandler(session).commit_operation_points(operation_points)

    assert lists_are_equal(
        session.query(LongOperationPoint).all(),
        [
            *long_operation_points,
            *other_long_operation_points,
        ],
    )
    assert lists_are_equal(
        session.query(ShortOperationPoint).all(),
        [
            *short_operation_points,
            *other_short_operation_points,
        ],
    )


def test_commit_fail_with_long_integration_error(
    long_operation_points,
    short_operation_points,
    session,
):
    long_operation_points[0].money_management_strategy_id = 1235
    operation_points = OperationPoints(long_operation_points, short_operation_points)

    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_operation_points(operation_points)


def test_commit_fail_with_short_integration_error(
    long_operation_points,
    short_operation_points,
    session,
):
    short_operation_points[0].money_management_strategy_id = 1235
    operation_points = OperationPoints(long_operation_points, short_operation_points)

    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_operation_points(operation_points)
