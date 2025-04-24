from database.models import MoneyManagementStrategy
from testing_utils.set_utils import set_of_tuples

NON_EXISTENT_ID = 123456789
NON_EXISTENT_IDENTIFIER = "atr-1000.1-2000.4-5000"


def test_all_with_empty_table():
    assert not MoneyManagementStrategy.query.all()


def test_all_with_table_items(other_money_management_strategies):
    assert set_of_tuples(MoneyManagementStrategy.query.all()) == set_of_tuples(
        other_money_management_strategies
    )


def test_from_id_with_empty_table():
    assert MoneyManagementStrategy.query.from_id(id=NON_EXISTENT_ID).one_or_none() is None


def test_from_id_with_table_items(other_money_management_strategies):
    item_1, item_2 = other_money_management_strategies

    assert (
        MoneyManagementStrategy.query.from_id(id=item_1.id).one_or_none().to_tuple()
        == item_1.to_tuple()
    )
    assert (
        MoneyManagementStrategy.query.from_id(id=item_2.id).one_or_none().to_tuple()
        == item_2.to_tuple()
    )
    assert MoneyManagementStrategy.query.from_id(id=NON_EXISTENT_ID).one_or_none() is None


def test_from_ids_with_empty_table():
    assert MoneyManagementStrategy.query.from_ids(ids=set()).all() == []
    assert MoneyManagementStrategy.query.from_ids(ids={NON_EXISTENT_ID}).all() == []


def test_from_ids_with_table_items(other_money_management_strategies):
    item_1, item_2 = other_money_management_strategies

    assert MoneyManagementStrategy.query.from_ids(ids=set()).all() == []
    assert MoneyManagementStrategy.query.from_ids(ids={NON_EXISTENT_ID}).all() == []
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_ids(ids={item_1.id}).all()
    ) == set_of_tuples([item_1])
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_ids(ids={item_2.id}).all()
    ) == set_of_tuples([item_2])
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_ids(ids={item_1.id, item_2.id}).all()
    ) == set_of_tuples(other_money_management_strategies)
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_ids(
            ids={NON_EXISTENT_ID, item_1.id, item_2.id}
        ).all()
    ) == set_of_tuples(other_money_management_strategies)


def test_from_identifier_with_empty_table():
    assert MoneyManagementStrategy.query.from_identifiers(identifiers=set()).all() == []
    assert (
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER}
        ).all()
        == []
    )


def test_from_identifier_with_table_items(other_money_management_strategies):
    item_1, item_2 = other_money_management_strategies

    assert MoneyManagementStrategy.query.from_identifiers(identifiers=set()).all() == []
    assert (
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER}
        ).all()
        == []
    )
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={item_1.identifier}
        ).all()
    ) == set_of_tuples([item_1])
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={item_2.identifier}
        ).all()
    ) == set_of_tuples([item_2])
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={item_1.identifier, item_2.identifier}
        ).all()
    ) == set_of_tuples(other_money_management_strategies)
    assert set_of_tuples(
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER, item_1.identifier, item_2.identifier}
        ).all()
    ) == set_of_tuples(other_money_management_strategies)
