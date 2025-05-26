import requests

from database.models import LongOperationPoint
from testing_utils.http_utils import parse_response

NON_EXISTENT_ID = 12345678


def test_empty_table(rust_endpoint, session):
    data = {"money_management_strategy_id": NON_EXISTENT_ID}

    response = requests.post(
        url=rust_endpoint("query_long_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_unmatched_items(other_long_operation_points, rust_endpoint, session):
    data = {"money_management_strategy_id": NON_EXISTENT_ID}

    response = requests.post(
        url=rust_endpoint("query_long_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert content.get("data") == []


def test_table_has_only_matched_items(
    other_long_operation_points,
    rust_endpoint,
    session,
):
    point_1, *_ = other_long_operation_points

    data = {"money_management_strategy_id": point_1.money_management_strategy_id}

    response = requests.post(
        url=rust_endpoint("query_long_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    expected_result = [
        item.to_dict(
            rules=("id", "money_management_strategy_id", "-long_balance", "-datetime")
        )
        for item in other_long_operation_points
    ]

    assert content["data"] == expected_result


def test_table_has_matched_and_unmatched_items(
    money_management_strategy_2,
    long_operation_points_data,
    other_long_operation_points,
    rust_endpoint,
    session,
):
    long_operation_points = [
        LongOperationPoint(
            **long_operation_point_data,
            money_management_strategy_id=money_management_strategy_2.id,
        )
        for long_operation_point_data in long_operation_points_data
    ]

    session.add_all(long_operation_points)
    session.commit()

    data = {"money_management_strategy_id": money_management_strategy_2.id}

    response = requests.post(
        url=rust_endpoint("query_long_operation_points_by_mms_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)
    expected_result = [
        item.to_dict(
            rules=("id", "money_management_strategy_id", "-long_balance", "-datetime")
        )
        for item in long_operation_points
    ]

    assert content["data"] == expected_result
