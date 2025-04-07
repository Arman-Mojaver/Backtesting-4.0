from database.handler import DatabaseHandler
from database.models import LongOperationPoint
from testing_utils.dict_utils import lists_are_equal


def test_commit_empty_items_does_nothing(session):
    DatabaseHandler(session).commit_long_operation_points([])

    assert not session.query(LongOperationPoint).all()


def test_commit_empty_items_with_existing_tables_items_does_nothing(
    other_long_operation_points,
    session,
):
    DatabaseHandler(session).commit_long_operation_points([])

    assert session.query(LongOperationPoint).all() == other_long_operation_points


def test_commit_success_one_with_empty_table(
    long_operation_point,
    session,
):
    DatabaseHandler(session).commit_long_operation_points([long_operation_point])

    assert session.query(LongOperationPoint).all() == [long_operation_point]


def test_commit_success_multiple_with_empty_table(
    long_operation_points,
    session,
):
    DatabaseHandler(session).commit_long_operation_points(long_operation_points)

    assert session.query(LongOperationPoint).all() == long_operation_points


def test_commit_success_one_with_existing_tables_items(
    other_long_operation_points,
    long_operation_point,
    session,
):
    DatabaseHandler(session).commit_long_operation_points([long_operation_point])

    assert lists_are_equal(
        session.query(LongOperationPoint).all(),
        [
            long_operation_point,
            *other_long_operation_points,
        ],
    )


def test_commit_success_multiple_with_existing_tables_items(
    other_long_operation_points,
    long_operation_points,
    session,
):
    DatabaseHandler(session).commit_long_operation_points(long_operation_points)

    assert lists_are_equal(
        session.query(LongOperationPoint).all(),
        [
            *long_operation_points,
            *other_long_operation_points,
        ],
    )
