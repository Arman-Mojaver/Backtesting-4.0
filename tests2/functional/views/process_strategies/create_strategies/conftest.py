import pytest


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
