from __future__ import annotations

import pytest
import requests

from testing_utils.http_utils import parse_response
from testing_utils.request_body_factory.strategy_factory import generate_strategies_data


@pytest.mark.parametrize(
    ("strategy_data", "global_min_annual_operation_count"),
    [
        (
            [],
            10.0,
        ),
        # Return none
        (
            generate_strategies_data(2, annual_operation_count=5.0),
            10.0,
        ),
        # Return all
        (
            generate_strategies_data(2, annual_operation_count=20.0),
            10.0,
        ),
        # Return all on threshold
        (
            generate_strategies_data(2, annual_operation_count=10.0),
            10.0,
        ),
        # Return partial items
        (
            generate_strategies_data(2, annual_operation_count=20.0)
            + generate_strategies_data(2, annual_operation_count=5.0),
            10.0,
        ),
    ],
)
def test_annual_operation_count(
    strategy_data,
    global_min_annual_operation_count,
    rust_endpoint,
):
    data = {
        "strategies": strategy_data,
        "strategy_profitability_parameters": {
            "global_min_annual_operation_count": global_min_annual_operation_count,
            "global_max_max_draw_down": 100.0,
            "global_min_annual_roi": 1.0,
        },
    }

    expected_strategy_data = [
        item
        for item in strategy_data
        if item["annual_operation_count"] >= global_min_annual_operation_count
    ]

    response = requests.post(
        url=rust_endpoint("strategy_profitability_test"),
        json=data,
        timeout=5,
    )
    content = parse_response(response)
    assert content.get("data") == expected_strategy_data


@pytest.mark.parametrize(
    ("strategy_data", "global_max_max_draw_down"),
    [
        (
            [],
            10.0,
        ),
        # Return none
        (
            generate_strategies_data(2, max_draw_down=20.0),
            10.0,
        ),
        # Return all
        (
            generate_strategies_data(2, max_draw_down=5.0),
            10.0,
        ),
        # Return all on threshold
        (
            generate_strategies_data(2, max_draw_down=10.0),
            10.0,
        ),
        # Return partial items
        (
            generate_strategies_data(2, max_draw_down=20.0)
            + generate_strategies_data(2, max_draw_down=5.0),
            10.0,
        ),
    ],
)
def test_max_draw_down(
    strategy_data,
    global_max_max_draw_down,
    rust_endpoint,
):
    data = {
        "strategies": strategy_data,
        "strategy_profitability_parameters": {
            "global_min_annual_operation_count": 300.0,
            "global_max_max_draw_down": global_max_max_draw_down,
            "global_min_annual_roi": 1.0,
        },
    }

    expected_strategy_data = [
        item
        for item in strategy_data
        if item["max_draw_down"] <= global_max_max_draw_down
    ]

    response = requests.post(
        url=rust_endpoint("strategy_profitability_test"),
        json=data,
        timeout=5,
    )
    content = parse_response(response)

    assert content.get("data") == expected_strategy_data


@pytest.mark.parametrize(
    ("strategy_data", "global_min_annual_roi"),
    [
        (
            [],
            10.0,
        ),
        # Return none
        (
            generate_strategies_data(2, annual_roi=5.0),
            10.0,
        ),
        # Return all
        (
            generate_strategies_data(2, annual_roi=20.0),
            10.0,
        ),
        # Return all on threshold
        (
            generate_strategies_data(2, annual_roi=10.0),
            10.0,
        ),
        # Return partial items
        (
            generate_strategies_data(2, annual_roi=20.0)
            + generate_strategies_data(2, annual_roi=5.0),
            10.0,
        ),
    ],
)
def test_annual_roi(
    strategy_data,
    global_min_annual_roi,
    rust_endpoint,
):
    data = {
        "strategies": strategy_data,
        "strategy_profitability_parameters": {
            "global_min_annual_operation_count": 300.0,
            "global_max_max_draw_down": 100.0,
            "global_min_annual_roi": global_min_annual_roi,
        },
    }

    expected_strategy_data = [
        item for item in strategy_data if item["annual_roi"] >= global_min_annual_roi
    ]

    response = requests.post(
        url=rust_endpoint("strategy_profitability_test"),
        json=data,
        timeout=5,
    )
    content = parse_response(response)
    assert content.get("data") == expected_strategy_data


def test_none(rust_endpoint):
    strategy_data = list(
        generate_strategies_data(2, annual_operation_count=20.0)
        + generate_strategies_data(2, max_draw_down=110.0)
        + generate_strategies_data(2, annual_roi=0.5),
    )

    global_min_annual_operation_count = 300.0
    global_max_max_draw_down = 100.0
    global_min_annual_roi = 1.0

    data = {
        "strategies": strategy_data,
        "strategy_profitability_parameters": {
            "global_min_annual_operation_count": global_min_annual_operation_count,
            "global_max_max_draw_down": global_max_max_draw_down,
            "global_min_annual_roi": global_min_annual_roi,
        },
    }

    response = requests.post(
        url=rust_endpoint("strategy_profitability_test"),
        json=data,
        timeout=5,
    )
    content = parse_response(response)
    assert content.get("data") == []


def test_all(rust_endpoint):
    strategy_data = list(
        generate_strategies_data(2, annual_operation_count=350.0)
        + generate_strategies_data(2, max_draw_down=70.0)
        + generate_strategies_data(2, annual_roi=9.0),
    )

    global_min_annual_operation_count = 300.0
    global_max_max_draw_down = 100.0
    global_min_annual_roi = 1.0

    data = {
        "strategies": strategy_data,
        "strategy_profitability_parameters": {
            "global_min_annual_operation_count": global_min_annual_operation_count,
            "global_max_max_draw_down": global_max_max_draw_down,
            "global_min_annual_roi": global_min_annual_roi,
        },
    }

    response = requests.post(
        url=rust_endpoint("strategy_profitability_test"),
        json=data,
        timeout=5,
    )
    content = parse_response(response)
    assert content.get("data") == strategy_data
