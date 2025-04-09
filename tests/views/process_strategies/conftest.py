import pytest

from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)


@pytest.fixture
def generate_long_operation_points():
    def _generate_long_operation_points(
        money_management_strategy_id,
        instrument,
        start_date,
        count,
    ):
        return generate_random_long_operation_points(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            start_date=start_date,
            count=count,
        )

    return _generate_long_operation_points


@pytest.fixture
def generate_short_operation_points(session):
    def _generate_short_operation_points(
        money_management_strategy_id,
        instrument,
        start_date,
        count,
    ):
        return generate_random_short_operation_points(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            start_date=start_date,
            count=count,
        )

    return _generate_short_operation_points
