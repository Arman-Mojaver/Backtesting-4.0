import pytest

from database.models import Indicator
from testing_utils.operation_points_utils.long_operation_points import (
    generate_random_long_operation_points,
)
from testing_utils.operation_points_utils.short_operation_points import (
    generate_random_short_operation_points,
)


@pytest.fixture
def strategy_response_defaults():
    def _defaults(overrides=None):
        values = {
            "long_operation_point_ids": [],
            "short_operation_point_ids": [],
            "strategy_data": {
                "annual_roi": 10.0,
                "annual_operation_count": 0.5,
                "max_draw_down": 2.0,
                "indicator_id": 1,
                "money_management_strategy_id": 1,
            },
        }
        if overrides:
            values.update(overrides)
        return values

    return _defaults


@pytest.fixture
def indicator(indicator_data):
    return Indicator(id=10, **indicator_data)


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
def generate_short_operation_points():
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
