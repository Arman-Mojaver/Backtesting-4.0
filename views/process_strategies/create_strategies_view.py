from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ValidationError, conlist
from sqlalchemy.exc import SQLAlchemyError

from database import session
from database.models import (
    Indicator,
    LongOperationPoint,
    LongOperationPointStrategy,
    MoneyManagementStrategy,
    ShortOperationPoint,
    ShortOperationPointStrategy,
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

        strategies, all_long_relationships, all_short_relationships = (
            self._create_strategies_and_relationships()
        )
        session.add_all(
            [
                *strategies,
                *all_long_relationships,
                *all_short_relationships,
            ]
        )
        self._commit()

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

    def _create_strategies_and_relationships(self):
        strategies, all_long_relationships, all_short_relationships = [], [], []
        for strategy_response in self.strategy_responses.data:
            strategy_data = strategy_response.strategy_data.model_dump()
            strategy = Strategy(**strategy_data)
            session.add(strategy)
            session.flush([strategy])

            long_relationships = self._create_long_operation_point_strategy_relationships(
                strategy=strategy,
                long_operation_point_ids=strategy_response.long_operation_point_ids,
            )
            short_relationships = (
                self._create_short_operation_point_strategy_relationships(
                    strategy=strategy,
                    short_operation_point_ids=strategy_response.short_operation_point_ids,
                )
            )

            strategies.append(strategy)
            all_long_relationships.extend(long_relationships)
            all_short_relationships.extend(short_relationships)

        return strategies, all_long_relationships, all_short_relationships

    def _create_short_operation_point_strategy_relationships(
        self,
        strategy: Strategy,
        short_operation_point_ids: list[int],
    ) -> list[ShortOperationPointStrategy]:
        short_operation_point_strategy_relationships = []

        for short_operation_point_id in short_operation_point_ids:
            short_operation_point = self.short_operation_points_by_id[
                short_operation_point_id
            ]
            self._validate_money_management_strategy_id(
                operation_point=short_operation_point,
                strategy=strategy,
            )
            short_relationship = ShortOperationPointStrategy(
                short_operation_point_id=short_operation_point.id,
                strategy_id=strategy.id,
            )
            short_operation_point_strategy_relationships.append(short_relationship)

        return short_operation_point_strategy_relationships

    def _create_long_operation_point_strategy_relationships(
        self,
        strategy: Strategy,
        long_operation_point_ids: list[int],
    ) -> list[LongOperationPointStrategy]:
        long_operation_point_strategy_relationships = []
        for long_operation_point_id in long_operation_point_ids:
            long_operation_point = self.long_operation_points_by_id[
                long_operation_point_id
            ]
            self._validate_money_management_strategy_id(
                operation_point=long_operation_point,
                strategy=strategy,
            )

            long_relationship = LongOperationPointStrategy(
                long_operation_point_id=long_operation_point.id,
                strategy_id=strategy.id,
            )
            long_operation_point_strategy_relationships.append(long_relationship)

        return long_operation_point_strategy_relationships

    @staticmethod
    def _commit() -> None:
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
