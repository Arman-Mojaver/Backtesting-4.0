import requests

from database.models import ShortOperationPoint
from testing_utils.http_utils import parse_response

NON_EXISTENT_ID = 12345678


def test_empty_table(rust_endpoint, session):
    data = {"money_management_strategy_id": NON_EXISTENT_ID}

    response = requests.post(
        url=rust_endpoint("query_short_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_unmatched_items(other_short_operation_points, rust_endpoint, session):
    data = {"money_management_strategy_id": NON_EXISTENT_ID}

    response = requests.post(
        url=rust_endpoint("query_short_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_only_matched_items(
    other_short_operation_points,
    rust_endpoint,
    session,
):
    point_1, *_ = other_short_operation_points

    data = {"money_management_strategy_id": point_1.money_management_strategy_id}

    response = requests.post(
        url=rust_endpoint("query_short_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    expected_result = [
        item.to_dict(
            rules=("id", "money_management_strategy_id", "-short_balance", "-datetime")
        )
        for item in other_short_operation_points
    ]

    assert content["data"] == expected_result


def test_table_has_matched_and_unmatched_items(
    money_management_strategy_2,
    short_operation_points_data,
    other_short_operation_points,
    rust_endpoint,
    session,
):
    short_operation_points = [
        ShortOperationPoint(
            **short_operation_point_data,
            money_management_strategy_id=money_management_strategy_2.id,
        )
        for short_operation_point_data in short_operation_points_data
    ]

    session.add_all(short_operation_points)
    session.commit()

    data = {"money_management_strategy_id": money_management_strategy_2.id}

    response = requests.post(
        url=rust_endpoint("query_short_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    expected_result = [
        item.to_dict(
            rules=("id", "money_management_strategy_id", "-short_balance", "-datetime")
        )
        for item in short_operation_points
    ]

    assert content["data"] == expected_result
