import pytest

from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ShortOperationPoint,
)


# Long operation points
def test_query_non_existent_operation_points(other_money_management_strategies):
    item_1, item_2 = other_money_management_strategies

    assert (
        MoneyManagementStrategy.query.filter_by(id=item_1.id).one().long_operation_points
        == []
    )
    assert (
        MoneyManagementStrategy.query.filter_by(id=item_2.id).one().long_operation_points
        == []
    )


def test_query_with_long_operation_points(
    other_money_management_strategies_with_long_operation_points,
    long_op_points,
    long_op_points_2,
):
    item_1, item_2 = other_money_management_strategies_with_long_operation_points

    assert {
        p.to_tuple()
        for p in MoneyManagementStrategy.query.filter_by(id=item_1.id)
        .one()
        .long_operation_points
    } == {p.to_tuple() for p in long_op_points}

    assert {
        p.to_tuple()
        for p in MoneyManagementStrategy.query.filter_by(id=item_2.id)
        .one()
        .long_operation_points
    } == {p.to_tuple() for p in long_op_points_2}


def test_cascade_delete_long_operation_points(
    other_money_management_strategies_with_long_operation_points,
    session,
):
    for item in session.query(LongOperationPoint):
        session.delete(item)

    session.commit()
    assert (
        session.query(MoneyManagementStrategy).all()
        == other_money_management_strategies_with_long_operation_points
    )


@pytest.mark.usefixtures("other_money_management_strategies_with_long_operation_points")
def test_cascade_delete_money_management_strategies_deletes_long_operation_points(
    session,
):
    for item in session.query(MoneyManagementStrategy):
        session.delete(item)

    session.commit()

    assert session.query(LongOperationPoint).all() == []


# Short operation points
def test_query_non_existent_short_operation_points(other_money_management_strategies):
    item_1, item_2 = other_money_management_strategies

    assert (
        MoneyManagementStrategy.query.filter_by(id=item_1.id).one().short_operation_points
        == []
    )
    assert (
        MoneyManagementStrategy.query.filter_by(id=item_2.id).one().short_operation_points
        == []
    )


def test_query_with_short_operation_points(
    other_money_management_strategies_with_short_operation_points,
    short_op_points,
    short_op_points_2,
):
    item_1, item_2 = other_money_management_strategies_with_short_operation_points

    assert {
        p.to_tuple()
        for p in MoneyManagementStrategy.query.filter_by(id=item_1.id)
        .one()
        .short_operation_points
    } == {p.to_tuple() for p in short_op_points}

    assert {
        p.to_tuple()
        for p in MoneyManagementStrategy.query.filter_by(id=item_2.id)
        .one()
        .short_operation_points
    } == {p.to_tuple() for p in short_op_points_2}


def test_cascade_delete_short_operation_points(
    other_money_management_strategies_with_short_operation_points,
    session,
):
    for item in session.query(ShortOperationPoint):
        session.delete(item)

    session.commit()
    assert (
        session.query(MoneyManagementStrategy).all()
        == other_money_management_strategies_with_short_operation_points
    )


@pytest.mark.usefixtures("other_money_management_strategies_with_short_operation_points")
def test_cascade_money_management_strategies_deletes_short_operation_points(session):
    for item in session.query(MoneyManagementStrategy):
        session.delete(item)

    session.commit()

    assert session.query(ShortOperationPoint).all() == []
