import pytest
from pydantic import ValidationError

from views.process_strategies.create_strategies_view import CreateStrategiesView


def test_empty_input_raises_error():
    with pytest.raises(ValidationError):
        CreateStrategiesView([]).run()


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"long_operation_point_ids": None},  # Wrong type
        {"short_operation_point_ids": None},  # Wrong type
        {"strategy_data": None},  # Missing strategy_data
        {"strategy_data": {"annual_roi": "wrong_type"}},  # Wrong type for annual_roi
        {"strategy_data": {"annual_operation_count": "wrong_type"}},  # Wrong type
        {"strategy_data": {"max_draw_down": "wrong_type"}},  # Wrong type
        {"strategy_data": {"indicator_id": "wrong_type"}},  # Wrong type
        {"strategy_data": {"money_management_strategy_id": "wrong_type"}},  # Wrong type
        {"strategy_data": {}},  # Missing all required fields in strategy_data
        {"strategy_data": {"annual_roi": None}},  # Missing annual_roi
        {
            "strategy_data": {"annual_operation_count": None}
        },  # Missing annual_operation_count
        {"strategy_data": {"max_draw_down": None}},  # Missing max_draw_down
        {"strategy_data": {"indicator_id": None}},  # Missing indicator_id
        {
            "strategy_data": {"money_management_strategy_id": None}
        },  # Missing money_management_strategy_id
        {
            "strategy_data": {
                "annual_operation_count": 0.5,
                "max_draw_down": 2.0,
                "indicator_id": 702,
                "money_management_strategy_id": 2,
            }
        },  # Missing annual_roi
        {
            "strategy_data": {
                "annual_roi": 10.0,
                "max_draw_down": 2.0,
                "indicator_id": 702,
                "money_management_strategy_id": 2,
            }
        },  # Missing annual_operation_count
        {
            "strategy_data": {
                "annual_roi": 10.0,
                "annual_operation_count": 0.5,
                "indicator_id": 702,
                "money_management_strategy_id": 2,
            }
        },  # Missing max_draw_down
        {
            "strategy_data": {
                "annual_roi": 10.0,
                "annual_operation_count": 0.5,
                "max_draw_down": 2.0,
                "money_management_strategy_id": 2,
            }
        },  # Missing indicator_id
        {
            "strategy_data": {
                "annual_roi": 10.0,
                "annual_operation_count": 0.5,
                "max_draw_down": 2.0,
                "indicator_id": 702,
            }
        },  # Missing money_management_strategy_id
    ],
)
def test_invalid_strategy_data(strategy_response_defaults, invalid_data):
    data = strategy_response_defaults(invalid_data)

    with pytest.raises(ValidationError):
        CreateStrategiesView([data]).run()
