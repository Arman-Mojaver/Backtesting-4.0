from database.handler import DatabaseHandler
from database.models import ShortOperationPoint
from testing_utils.dict_utils import lists_are_equal


def test_commit_empty_items_does_nothing(session):
    DatabaseHandler(session).commit_short_operation_points([])

    assert not session.query(ShortOperationPoint).all()


def test_commit_empty_items_with_existing_tables_items_does_nothing(
    other_short_operation_points,
    session,
):
    DatabaseHandler(session).commit_short_operation_points([])

    assert session.query(ShortOperationPoint).all() == other_short_operation_points


def test_commit_success_one_with_empty_table(
    short_operation_point,
    session,
):
    DatabaseHandler(session).commit_short_operation_points([short_operation_point])

    assert session.query(ShortOperationPoint).all() == [short_operation_point]


def test_commit_success_multiple_with_empty_table(
    short_operation_points,
    session,
):
    DatabaseHandler(session).commit_short_operation_points(short_operation_points)

    assert session.query(ShortOperationPoint).all() == short_operation_points


def test_commit_success_one_with_existing_tables_items(
    other_short_operation_points,
    short_operation_point,
    session,
):
    DatabaseHandler(session).commit_short_operation_points([short_operation_point])

    assert lists_are_equal(
        session.query(ShortOperationPoint).all(),
        [
            short_operation_point,
            *other_short_operation_points,
        ],
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
