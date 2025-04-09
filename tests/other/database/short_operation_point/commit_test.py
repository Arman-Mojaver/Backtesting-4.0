import pytest
from sqlalchemy.exc import IntegrityError

from database.handler import DatabaseHandler
from database.models import ShortOperationPoint
from testing_utils.dict_utils import lists_are_equal


def test_commit_success_multiple_with_empty_table(
    short_operation_points,
    session,
):
    DatabaseHandler(session).commit_short_operation_points(short_operation_points)

    assert lists_are_equal(
        session.query(ShortOperationPoint).all(), short_operation_points
    )


def test_commit_success_multiple_with_existing_tables_items(
    other_short_operation_points,
    short_operation_points,
    session,
):
    DatabaseHandler(session).commit_short_operation_points(short_operation_points)

    assert lists_are_equal(
        session.query(ShortOperationPoint).all(),
        [
            *short_operation_points,
            *other_short_operation_points,
        ],
    )


def test_commit_fail_with_integration_error(
    short_operation_points,
    session,
):
    short_operation_points[0].money_management_strategy_id = 1235
    with pytest.raises(IntegrityError):
        DatabaseHandler(session).commit_short_operation_points(short_operation_points)
