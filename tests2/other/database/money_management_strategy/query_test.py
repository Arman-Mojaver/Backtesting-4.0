import pytest

from database.models import MoneyManagementStrategy
from database.models.money_management_strategy import NonExistentIdError

NON_EXISTENT_ID = 123456789


def test_all_with_empty_table(session):
    assert not MoneyManagementStrategy.query.all()


def test_all_with_table_items(session, other_money_management_strategies):
    assert MoneyManagementStrategy.query.all() == other_money_management_strategies


def test_from_ids_with_empty_ids_raises_error(session):
    with pytest.raises(NonExistentIdError):
        MoneyManagementStrategy.query.from_ids(ids=set())


@pytest.mark.usefixtures("other_money_management_strategies")
def test_from_ids_with_empty_ids_raises_error_with_table_items(session):
    with pytest.raises(NonExistentIdError):
        MoneyManagementStrategy.query.from_ids(ids=set())


def test_from_ids_with_id_mismatch(
    session,
    other_money_management_strategies,
):
    item_1, item_2 = other_money_management_strategies

    with pytest.raises(NonExistentIdError):
        MoneyManagementStrategy.query.from_ids(
            ids={NON_EXISTENT_ID, item_1.id, item_2.id}
        )


def test_from_ids_with_table_items(
    session,
    other_money_management_strategies,
):
    item_1, item_2 = other_money_management_strategies

    assert MoneyManagementStrategy.query.from_ids(ids={item_1.id}) == [item_1]
    assert MoneyManagementStrategy.query.from_ids(ids={item_2.id}) == [item_2]
    assert (
        MoneyManagementStrategy.query.from_ids(ids={item_1.id, item_2.id})
        == other_money_management_strategies
    )
