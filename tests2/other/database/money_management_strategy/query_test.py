from database.models import MoneyManagementStrategy

NON_EXISTENT_ID = 123456789
NON_EXISTENT_IDENTIFIER = "atr-1000.1-2000.4-5000"


def test_all_with_empty_table(session):
    assert not MoneyManagementStrategy.query.all()


def test_all_with_table_items(session, other_money_management_strategies):
    assert MoneyManagementStrategy.query.all() == other_money_management_strategies


def test_from_ids_with_empty_table(session):
    assert MoneyManagementStrategy.query.from_ids(ids=set()) == []
    assert MoneyManagementStrategy.query.from_ids(ids={NON_EXISTENT_ID}) == []


def test_from_ids_with_table_items(
    session,
    other_money_management_strategies,
):
    item_1, item_2 = other_money_management_strategies

    assert MoneyManagementStrategy.query.from_ids(ids=set()) == []
    assert MoneyManagementStrategy.query.from_ids(ids={NON_EXISTENT_ID}) == []
    assert MoneyManagementStrategy.query.from_ids(ids={item_1.id}) == [item_1]
    assert MoneyManagementStrategy.query.from_ids(ids={item_2.id}) == [item_2]
    assert (
        MoneyManagementStrategy.query.from_ids(ids={item_1.id, item_2.id})
        == other_money_management_strategies
    )
    assert (
        MoneyManagementStrategy.query.from_ids(
            ids={NON_EXISTENT_ID, item_1.id, item_2.id}
        )
        == other_money_management_strategies
    )


def test_from_identifier_with_empty_table(session):
    assert MoneyManagementStrategy.query.from_identifiers(identifiers=set()) == []
    assert (
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER}
        )
        == []
    )


def test_from_identifier_with_table_items(
    session,
    other_money_management_strategies,
):
    item_1, item_2 = other_money_management_strategies

    assert MoneyManagementStrategy.query.from_identifiers(identifiers=set()) == []
    assert (
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER}
        )
        == []
    )
    assert MoneyManagementStrategy.query.from_identifiers(
        identifiers={item_1.identifier}
    ) == [item_1]
    assert MoneyManagementStrategy.query.from_identifiers(
        identifiers={item_2.identifier}
    ) == [item_2]
    assert (
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={item_1.identifier, item_2.identifier}
        )
        == other_money_management_strategies
    )
    assert (
        MoneyManagementStrategy.query.from_identifiers(
            identifiers={NON_EXISTENT_IDENTIFIER, item_1.identifier, item_2.identifier}
        )
        == other_money_management_strategies
    )
