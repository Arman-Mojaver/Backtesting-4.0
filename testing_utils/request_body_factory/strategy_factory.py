from __future__ import annotations


def generate_strategies_data(
    count: int,
    annual_operation_count: float = 365.0,
    max_draw_down: float = 90.0,
    annual_roi: float = 2.0,
) -> list[dict]:
    return [
        {
            "money_management_strategy_id": 300 + i,
            "indicator_id": 9000 + 1,
            "annual_operation_count": annual_operation_count,
            "max_draw_down": max_draw_down,
            "annual_roi": annual_roi,
        }
        for i in range(count)
    ]
