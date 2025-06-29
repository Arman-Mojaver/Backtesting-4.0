from __future__ import annotations

import requests

from database.models import (
    LongOperationPointStrategy,
    ShortOperationPointStrategy,
    Strategy,
)
from testing_utils.http_utils import parse_response
from testing_utils.set_utils import set_of_tuples


def test_commit_strategy(rust_endpoint, strategy_1, session):
    data = {
        "strategy_groups": [
            {
                "strategy": strategy_1.to_dict(),
                "long_operation_point_ids": [],
                "short_operation_point_ids": [],
            }
        ]
    }

    response = requests.post(
        url=rust_endpoint("commit_strategy_groups_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert len(content.get("data", [])) == len(data["strategy_groups"])
    assert set_of_tuples(Strategy.query.all()) == set_of_tuples([strategy_1])
    assert session.query(LongOperationPointStrategy).all() == []
    assert session.query(ShortOperationPointStrategy).all() == []


def test_commit_strategies(rust_endpoint, strategy_1, strategy_2, session):
    data = {
        "strategy_groups": [
            {
                "strategy": strategy_1.to_dict(),
                "long_operation_point_ids": [],
                "short_operation_point_ids": [],
            },
            {
                "strategy": strategy_2.to_dict(),
                "long_operation_point_ids": [],
                "short_operation_point_ids": [],
            },
        ]
    }

    response = requests.post(
        url=rust_endpoint("commit_strategy_groups_test"),
        json=data,
        timeout=5,
    )

    content = parse_response(response)

    assert len(content.get("data", [])) == len(data["strategy_groups"])
    assert set_of_tuples(Strategy.query.all()) == set_of_tuples([strategy_1, strategy_2])
    assert session.query(LongOperationPointStrategy).all() == []
    assert session.query(ShortOperationPointStrategy).all() == []
