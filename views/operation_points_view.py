from __future__ import annotations

from typing import TYPE_CHECKING

from config import config  # type: ignore[attr-defined]
from config.logging_config.log_decorators import log_on_end, log_on_start
from controllers.create_multiple_balance_point_controller import (
    BalancePointCreateMultipleController,
)
from controllers.create_multiple_operation_point_controller import (
    OperationPointsCreateOneController,
)
from exceptions import (
    LargeAtrParameterError,
    NoMoneyManagementStrategiesError,
    NoResampledPointsError,
)
from logger import log
from models.operation_point import OperationPoints
from schemas.instruments_schema import EnabledInstrumentsMismatchError
from utils.dict_utils import dict_multi_by_key

if TYPE_CHECKING:
    from database.models import (
        LongOperationPoint,
        MoneyManagementStrategy,
        ResampledPointD1,
        ShortOperationPoint,
    )


class OperationPointsCreateMultipleView:
    def __init__(
        self,
        resampled_points: list[ResampledPointD1],
        money_management_strategies: list[MoneyManagementStrategy],
        enabled_instruments: tuple[str, ...] = config.ENABLED_INSTRUMENTS,
    ):
        self.resampled_points: list[ResampledPointD1] = resampled_points
        self.resampled_points_by_instrument = dict_multi_by_key(
            key="instrument",
            items=self.resampled_points,
        )
        self.money_management_strategies: list[MoneyManagementStrategy] = (
            money_management_strategies
        )
        self.enabled_instruments: tuple[str, ...] = enabled_instruments

        self.long_operation_points: list[LongOperationPoint] = []
        self.short_operation_points: list[ShortOperationPoint] = []

    @log_on_start("Creating Operation Points")
    @log_on_end("Finished OperationPointsCreateMultipleView")
    def run(self) -> OperationPoints:
        self._validate_resampled_points_exist()
        self._validate_money_management_strategy_exists()
        self._validate_atr_parameter()
        self._validate_enabled_instruments()
        self.long_operation_points, self.short_operation_points = self._run_controller()
        return OperationPoints(
            long_operation_points=self.long_operation_points,
            short_operation_points=self.short_operation_points,
        )

    def _validate_resampled_points_exist(self):
        if not self.resampled_points_by_instrument:
            err = "No resampled points in db"
            raise NoResampledPointsError(err)

    def _validate_money_management_strategy_exists(self):
        if not self.money_management_strategies:
            err = "No money management strategies in db"
            raise NoMoneyManagementStrategiesError(err)

    def _validate_atr_parameter(self):
        atr_parameters = [
            money_management_strategy.parameters["atr_parameter"]
            for money_management_strategy in self.money_management_strategies
        ]
        for resampled_points in self.resampled_points_by_instrument.values():
            if any(
                len(resampled_points) < atr_parameter for atr_parameter in atr_parameters
            ):
                err = (
                    "Not enough resampled points for given atr_parameter"
                    f"{len(resampled_points)=}, {atr_parameters=}"
                )

                raise LargeAtrParameterError(err)

    def _validate_enabled_instruments(self):
        instruments = self.resampled_points_by_instrument.keys()
        if set(self.enabled_instruments) != set(instruments):
            err = (
                f"Mismatch between enabled instruments and file instruments: "
                f"{config.ENABLED_INSTRUMENTS=}, {instruments=}"
            )
            raise EnabledInstrumentsMismatchError(err)

    def _run_controller(
        self,
    ) -> tuple[list[LongOperationPoint], list[ShortOperationPoint]]:
        all_long_operation_points, all_short_operation_points = [], []
        for instrument, resampled_points in self.resampled_points_by_instrument.items():
            log.info(f"Processing instrument: {instrument}")
            controller = BalancePointCreateMultipleController(
                resampled_points=resampled_points
            )
            long_balance_points_by_date, short_balance_points_by_date = controller.run()

            for money_management_strategy in self.money_management_strategies:
                log.info(
                    "Creating Operation Points for money management strategy: "
                    f"{money_management_strategy.identifier}"
                )
                controller = OperationPointsCreateOneController(
                    money_management_strategy=money_management_strategy,
                    resampled_points=resampled_points,
                    long_balance_points_by_date=long_balance_points_by_date,
                    short_balance_points_by_date=short_balance_points_by_date,
                )
                long_operation_points, short_operation_points = controller.run()
                all_long_operation_points.extend(long_operation_points)
                all_short_operation_points.extend(short_operation_points)

        return all_long_operation_points, all_short_operation_points
