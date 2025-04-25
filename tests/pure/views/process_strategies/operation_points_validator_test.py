import pytest

from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)
from views.process_strategies.operation_points_validator import (
    InvalidOperationPointsError,
    OperationPoints,
    OperationPointsValidator,
)


@pytest.mark.parametrize(
    ("money_management_strategy_id", "long_operation_points", "short_operation_points"),
    [
        (1, [], []),
        (
            1,
            [],
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
        ),
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-01", 10),
            [],
        ),
        # instrument mismatch
        (
            1,
            generate_random_long_operation_points(1, "USDCAD", "2024-01-01", 1)
            + generate_random_long_operation_points(1, "EURUSD", "2024-01-02", 9),
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
        ),
        # date mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-10", 10),
            generate_random_short_operation_points(1, "EURUSD", "2024-01-01", 10),
        ),
        # money management strategy mismatch
        (
            1,
            generate_random_long_operation_points(1, "EURUSD", "2024-01-01", 1)
            + generate_random_long_operation_points(2, "EURUSD", "2024-01-02", 9),
            generate_random_short_operation_points(2, "EURUSD", "2024-01-01", 10),
        ),
    ],
)
def test_operation_points_validation_raises(
    money_management_strategy_id, long_operation_points, short_operation_points
):
    with pytest.raises(InvalidOperationPointsError):
        OperationPointsValidator(
            money_management_strategy_id, long_operation_points, short_operation_points
        ).run()


def test_success():
    money_management_strategy_id = 1
    long_operation_points = generate_random_long_operation_points(
        money_management_strategy_id,
        "EURUSD",
        "2024-01-01",
        10,
    )

    short_operation_points = generate_random_short_operation_points(
        money_management_strategy_id,
        "EURUSD",
        "2024-01-01",
        10,
    )
    assert OperationPointsValidator(
        money_management_strategy_id,
        long_operation_points,
        short_operation_points,
    ).run() == OperationPoints(
        long_operation_points=long_operation_points,
        short_operation_points=short_operation_points,
    )
