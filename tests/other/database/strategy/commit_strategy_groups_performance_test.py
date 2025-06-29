import time

import pytest
import requests
from sqlalchemy import delete

from database.models import (
    Indicator,
    LongOperationPoint,
    MoneyManagementStrategy,
    ShortOperationPoint,
    Strategy,
)
from testing_utils.request_body_factory.indicator_factory import generate_rsi_indicators
from testing_utils.request_body_factory.operation_points_factory import (
    OperationPointsFactory,
)
from testing_utils.request_body_factory.strategy_factory import (
    generate_strategies_data_with_ids,
)

STRATEGY_GROUP_COUNT = 200
OPERATION_POINTS_COUNT = 600


@pytest.fixture(autouse=True)
def _clean_table(session):
    yield
    session.rollback()
    session.execute(delete(Strategy))
    session.execute(delete(LongOperationPoint))
    session.execute(delete(ShortOperationPoint))
    session.execute(delete(MoneyManagementStrategy))
    session.execute(delete(Indicator))
    session.commit()


@pytest.mark.skip(reason="Performance test, takes a long time")
def test_commit_strategy_groups_performance(
    rust_endpoint,
    money_management_strategy,
    session,
):
    operation_points_factory = OperationPointsFactory(
        instrument="EURUSD",
        mm_strategy_id=money_management_strategy.id,
        start_date="2022-01-01",
        end_date="2037-01-01",
    )

    long_operation_points = operation_points_factory.long_operation_points
    short_operation_points = operation_points_factory.short_operation_points

    indicators = generate_rsi_indicators(count=STRATEGY_GROUP_COUNT)

    session.add_all(
        [
            money_management_strategy,
            *long_operation_points,
            *short_operation_points,
            *indicators,
        ]
    )
    session.commit()

    long_operation_point_sample = [
        long_operation_points[
            (i * (len(long_operation_points) // OPERATION_POINTS_COUNT) + 3)
            % len(long_operation_points)
        ]
        for i in range(OPERATION_POINTS_COUNT)
    ]

    short_operation_point_sample = [
        short_operation_points[
            (i * (len(short_operation_points) // OPERATION_POINTS_COUNT) + 3)
            % len(short_operation_points)
        ]
        for i in range(600)
    ]

    long_operation_point_ids = [i.id for i in long_operation_point_sample]
    short_operation_point_ids = [i.id for i in short_operation_point_sample]

    strategies = generate_strategies_data_with_ids(
        indicator_ids=[i.id for i in indicators],
        money_management_strategy_ids=[money_management_strategy.id],
    )

    data = {
        "strategy_groups": [
            {
                "strategy": strategy,
                "long_operation_point_ids": long_operation_point_ids,
                "short_operation_point_ids": short_operation_point_ids,
            }
            for strategy in strategies
        ]
    }

    print("Sending request")  # noqa: T201
    start = time.time()
    requests.post(
        url=rust_endpoint("commit_strategy_groups_test"),
        json=data,
        timeout=30,
    )

    elapsed = time.time() - start
    print(f"Request time: {round(elapsed, 2)}s")  # noqa: T201

    assert session.query(Strategy).count() == STRATEGY_GROUP_COUNT

    """
        Single threaded, for loops:
            Process time: 21.12s
    """
