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


def test_commit_strategies_with_existing_strategies(
    rust_endpoint,
    strategy_1,
    strategy_2,
    other_strategies,
    session,
):
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
    assert set_of_tuples(Strategy.query.all()) == set_of_tuples(
        [strategy_1, strategy_2, *other_strategies]
    )
    assert session.query(LongOperationPointStrategy).all() == []
    assert session.query(ShortOperationPointStrategy).all() == []


def test_one_strategy_one_long_one_short(
    rust_endpoint,
    strategy_1,
    other_long_operation_points,
    other_short_operation_points,
    session,
):
    long_operation_point, *_ = other_long_operation_points
    short_operation_point, *_ = other_short_operation_points

    data = {
        "strategy_groups": [
            {
                "strategy": strategy_1.to_dict(),
                "long_operation_point_ids": [long_operation_point.id],
                "short_operation_point_ids": [short_operation_point.id],
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
    assert set_of_tuples(
        session.query(LongOperationPointStrategy).all()
    ) == set_of_tuples(
        [
            LongOperationPointStrategy(
                long_operation_point_id=long_operation_point.id,
                strategy_id=Strategy.query.first().id,
            )
        ]
    )
    assert set_of_tuples(
        session.query(ShortOperationPointStrategy).all()
    ) == set_of_tuples(
        [
            ShortOperationPointStrategy(
                short_operation_point_id=short_operation_point.id,
                strategy_id=Strategy.query.first().id,
            )
        ]
    )


def test_two_strategy_one_long_one_short_each(  # noqa: PLR0913
    rust_endpoint,
    strategy_1,
    strategy_2,
    other_long_operation_points,
    other_short_operation_points,
    session,
):
    long_operation_point_1, long_operation_point_2 = other_long_operation_points
    short_operation_point_1, short_operation_point_2 = other_short_operation_points

    data = {
        "strategy_groups": [
            {
                "strategy": strategy_1.to_dict(),
                "long_operation_point_ids": [long_operation_point_1.id],
                "short_operation_point_ids": [short_operation_point_1.id],
            },
            {
                "strategy": strategy_2.to_dict(),
                "long_operation_point_ids": [long_operation_point_2.id],
                "short_operation_point_ids": [short_operation_point_2.id],
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
    assert set_of_tuples(Strategy.query.all()) == set_of_tuples([strategy_1, strategy_2])
    assert set_of_tuples(
        session.query(LongOperationPointStrategy).all()
    ) == set_of_tuples(
        [
            LongOperationPointStrategy(
                long_operation_point_id=long_operation_point_1.id,
                strategy_id=Strategy.query.all()[0].id,
            ),
            LongOperationPointStrategy(
                long_operation_point_id=long_operation_point_2.id,
                strategy_id=Strategy.query.all()[1].id,
            )
        ]
    )
    assert set_of_tuples(
        session.query(ShortOperationPointStrategy).all()
    ) == set_of_tuples(
        [
            ShortOperationPointStrategy(
                short_operation_point_id=short_operation_point_1.id,
                strategy_id=Strategy.query.all()[0].id,
            ),
            ShortOperationPointStrategy(
                short_operation_point_id=short_operation_point_2.id,
                strategy_id=Strategy.query.all()[1].id,
            )
        ]
    )


def test_one_strategy_mixed_operation_points_count(  # noqa: PLR0913
    rust_endpoint,
    strategy_1,
    strategy_2,
    other_long_operation_points,
    other_short_operation_points,
    session,
):
    long_operation_point_1, long_operation_point_2 = other_long_operation_points
    short_operation_point_1, short_operation_point_2 = other_short_operation_points

    data = {
        "strategy_groups": [
            {
                "strategy": strategy_1.to_dict(),
                "long_operation_point_ids": [
                    long_operation_point_1.id,
                    long_operation_point_2.id,
                ],
                "short_operation_point_ids": [short_operation_point_1.id],
            },
            {
                "strategy": strategy_2.to_dict(),
                "long_operation_point_ids": [long_operation_point_2.id],
                "short_operation_point_ids": [
                    short_operation_point_1.id,
                    short_operation_point_2.id,
                ],
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
    assert set_of_tuples(Strategy.query.all()) == set_of_tuples([strategy_1, strategy_2])

    strategy_1, strategy_2 = Strategy.query.all()

    assert set_of_tuples(
        session.query(LongOperationPointStrategy).all()
    ) == set_of_tuples(
        [
            LongOperationPointStrategy(
                long_operation_point_id=long_operation_point_1.id,
                strategy_id=strategy_1.id,
            ),
            LongOperationPointStrategy(
                long_operation_point_id=long_operation_point_2.id,
                strategy_id=strategy_1.id,
            ),
            LongOperationPointStrategy(
                long_operation_point_id=long_operation_point_2.id,
                strategy_id=strategy_2.id,
            )
        ]
    )
    assert set_of_tuples(
        session.query(ShortOperationPointStrategy).all()
    ) == set_of_tuples(
        [
            ShortOperationPointStrategy(
                short_operation_point_id=short_operation_point_1.id,
                strategy_id=strategy_1.id,
            ),
            ShortOperationPointStrategy(
                short_operation_point_id=short_operation_point_1.id,
                strategy_id=strategy_2.id,
            ),
            ShortOperationPointStrategy(
                short_operation_point_id=short_operation_point_2.id,
                strategy_id=strategy_2.id,
            )
        ]
    )
