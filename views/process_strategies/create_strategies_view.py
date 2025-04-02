from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ValidationError, conlist


class NonExistentIdError(Exception):
    pass


class StrategyData(BaseModel):
    annual_operation_count: float
    annual_roi: float
    max_draw_down: float
    money_management_strategy_id: int
    indicator_id: int


class StrategyResponse(BaseModel):
    strategy_data: StrategyData
    long_operation_point_ids: list[int]
    short_operation_point_ids: list[int]


class StrategyResponses(BaseModel):
    data: conlist(StrategyResponse, min_length=1)


class CreateStrategiesView:
    def __init__(self, data: list[dict[str, Any]]):
        self.data: list[dict[str, Any]] = data

    def run(self) -> None:
        try:
            StrategyResponses.model_validate({"data": self.data})
        except ValidationError:
            raise
