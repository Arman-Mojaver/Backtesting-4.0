from __future__ import annotations


def generate_strategies_data(
    count: int,
    annual_operation_count: float = 365.0,
    max_draw_down: float = 90.0,
    annual_roi: float = 3.0,
) -> list[dict]:
    return [
        {
            "instrument": "EURUSD",
            "money_management_strategy_id": 300 + i,
            "indicator_id": 9000 + i,
            "annual_operation_count": annual_operation_count,
            "max_draw_down": max_draw_down,
            "annual_roi": annual_roi,
        }
        for i in range(count)
    ]


def generate_strategies_data_with_ids(
    indicator_ids: list[int],
    money_management_strategy_ids: list[int],
    annual_operation_count: float = 365.0,
    max_draw_down: float = 90.0,
    annual_roi: float = 3.0,
) -> list[dict]:
    items = []
    for money_management_strategy_id in money_management_strategy_ids:
        for indicator_id in indicator_ids:
            items.append(  # noqa: PERF401
                {
                    "instrument": "EURUSD",
                    "money_management_strategy_id": money_management_strategy_id,
                    "indicator_id": indicator_id,
                    "annual_operation_count": annual_operation_count,
                    "max_draw_down": max_draw_down,
                    "annual_roi": annual_roi,
                }
            )

    return items
