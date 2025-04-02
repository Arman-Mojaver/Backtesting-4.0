from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ValidationError, conlist

from database.models import (
    Indicator,
    LongOperationPoint,
    MoneyManagementStrategy,
    ShortOperationPoint,
    Strategy,
)


class NonExistentIdError(Exception):
    pass


class MismatchedIdError(Exception):
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

    def money_management_strategy_ids(self) -> set[int]:
        return {
            strategy_response.strategy_data.money_management_strategy_id
            for strategy_response in self.data
        }

    def indicator_ids(self) -> set[int]:
        return {
            strategy_response.strategy_data.indicator_id
            for strategy_response in self.data
        }

    def long_operation_point_ids(self) -> set[int]:
        ids = []
        for strategy_response in self.data:
            ids.extend(strategy_response.long_operation_point_ids)
        return set(ids)

    def short_operation_point_ids(self) -> set[int]:
        ids = []
        for strategy_response in self.data:
            ids.extend(strategy_response.short_operation_point_ids)
        return set(ids)


class CreateStrategiesView:
    def __init__(self, data: list[dict[str, Any]]):
        self.data: list[dict[str, Any]] = data

        self.strategy_responses: StrategyResponses | None = None
        self.long_operation_points_by_id: dict[int, LongOperationPoint] | None = None
        self.short_operation_points_by_id: dict[int, ShortOperationPoint] | None = None

    def run(self) -> None:
        self.strategy_responses = self._get_strategy_responses()
        self._validate_money_management_strategy_ids()
        self._validate_indicator_ids()

        self.long_operation_points_by_id = self._get_long_operation_points_by_id()
        self._validate_long_operation_point_ids()

        self.short_operation_points_by_id = self._get_short_operation_points_by_id()
        self._validate_short_operation_point_ids()
        self._validate_mismatched_ids()

    def _get_strategy_responses(self) -> StrategyResponses:
        try:
            return StrategyResponses.model_validate({"data": self.data})
        except ValidationError:
            raise

    def _validate_money_management_strategy_ids(self) -> None:
        money_management_strategies = MoneyManagementStrategy.query.from_ids(
            self.strategy_responses.money_management_strategy_ids()
        )
        money_management_strategy_ids = {item.id for item in money_management_strategies}

        symmetric_difference = (
            money_management_strategy_ids
            ^ self.strategy_responses.money_management_strategy_ids()
        )

        if symmetric_difference:
            err = (
                "MoneyManagementStrategy IDs did not match. "
                f"Symmetric difference: {symmetric_difference}"
            )
            raise NonExistentIdError(err)

    def _validate_indicator_ids(self) -> None:
        indicators = Indicator.query.from_ids(self.strategy_responses.indicator_ids())
        indicators_ids = {item.id for item in indicators}

        symmetric_difference = indicators_ids ^ self.strategy_responses.indicator_ids()

        if symmetric_difference:
            err = (
                "Indicator IDs did not match. "
                f"Symmetric difference: {symmetric_difference}"
            )
            raise NonExistentIdError(err)

    def _get_long_operation_points_by_id(self) -> dict[int, LongOperationPoint]:
        return LongOperationPoint.query.from_ids_by_id(
            ids=self.strategy_responses.long_operation_point_ids()
        )

    def _validate_long_operation_point_ids(self) -> None:
        symmetric_difference = (
            set(self.long_operation_points_by_id.keys())
            ^ self.strategy_responses.long_operation_point_ids()
        )

        if symmetric_difference:
            err = (
                "LongOperationPoint IDs did not match. "
                f"Symmetric difference: {symmetric_difference}"
            )
            raise NonExistentIdError(err)

    def _get_short_operation_points_by_id(self) -> dict[int, ShortOperationPoint]:
        return ShortOperationPoint.query.from_ids_by_id(
            ids=self.strategy_responses.short_operation_point_ids()
        )

    def _validate_short_operation_point_ids(self) -> None:
        symmetric_difference = (
            set(self.short_operation_points_by_id.keys())
            ^ self.strategy_responses.short_operation_point_ids()
        )

        if symmetric_difference:
            err = (
                "ShortOperationPoint IDs did not match. "
                f"Symmetric difference: {symmetric_difference}"
            )
            raise NonExistentIdError(err)

    @staticmethod
    def _validate_money_management_strategy_id(
        operation_point: LongOperationPoint | ShortOperationPoint,
        strategy: Strategy,
    ) -> None:
        if (
            operation_point.money_management_strategy_id
            != strategy.money_management_strategy_id
        ):
            err = (
                "Mismatch between Operation Point's "
                "MoneyManagementStrategy ID and Strategy's MoneyManagementStrategy ID"
                f"{operation_point.money_management_strategy_id=}, "
                f"{strategy.money_management_strategy_id=}"
            )
            raise MismatchedIdError(err)

    def _validate_mismatched_ids(self):
        for strategy_response in self.strategy_responses.data:
            strategy = Strategy(**strategy_response.strategy_data.model_dump())

            for long_operation_point_id in strategy_response.long_operation_point_ids:
                long_operation_point = self.long_operation_points_by_id[
                    long_operation_point_id
                ]
                self._validate_money_management_strategy_id(
                    operation_point=long_operation_point,
                    strategy=strategy,
                )

            for short_operation_point_id in strategy_response.short_operation_point_ids:
                short_operation_point = self.short_operation_points_by_id[
                    short_operation_point_id
                ]
                self._validate_money_management_strategy_id(
                    operation_point=short_operation_point,
                    strategy=strategy,
                )
