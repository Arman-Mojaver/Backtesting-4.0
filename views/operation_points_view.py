from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError

from config import config  # type: ignore[attr-defined]
from config.logging_config.log_decorators import log_on_end
from controllers.create_multiple_operation_point_controller import (
    OperationPointsCreateOneController,
)
from database import session
from database.models import (
    LongOperationPoint,
    MoneyManagementStrategy,
    ResampledPointD1,
    ShortOperationPoint,
)
from exceptions import (
    LargeAtrParameterError,
    NoMoneyManagementStrategiesError,
    NoResampledPointsError,
)
from schemas.instruments_schema import EnabledInstrumentsMismatchError


class OperationPointsCreateMultipleView:
    def __init__(self):
        self.resampled_points = ResampledPointD1.query.all()
        self.money_management_strategies = MoneyManagementStrategy.query.all()

        self.all_long_operation_points: list[LongOperationPoint] = []
        self.all_short_operation_points: list[ShortOperationPoint] = []

    def run(self) -> None:
        self._validate_resampled_points_exist()
        self._validate_money_management_strategy_exists()
        self._validate_atr_parameter()
        self._validate_enabled_instruments()
        self.all_long_operation_points, self.all_short_operation_points = (
            self._run_controller()
        )
        self._add_to_session()
        self._commit()

    def _validate_resampled_points_exist(self):
        if not self.resampled_points:
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
        if any(
            len(self.resampled_points) < atr_parameter for atr_parameter in atr_parameters
        ):
            err = (
                "Not enough resampled points for given atr_parameter"
                f"{len(self.resampled_points)=}, {atr_parameters=}"
            )

            raise LargeAtrParameterError(err)

    def _validate_enabled_instruments(self):
        instruments = [point.instrument for point in self.resampled_points]
        if set(config.ENABLED_INSTRUMENTS) != set(instruments):
            err = (
                f"Mismatch between enabled instruments and file instruments: "
                f"{config.ENABLED_INSTRUMENTS=}, {instruments=}"
            )
            raise EnabledInstrumentsMismatchError(err)

    def _run_controller(self):
        all_long_operation_points, all_short_operation_points = [], []
        for money_management_strategy in self.money_management_strategies:
            controller = OperationPointsCreateOneController(
                money_management_strategy=money_management_strategy,
                resampled_points=self.resampled_points,
            )
            long_operation_points, short_operation_points = controller.run()

            all_long_operation_points.extend(long_operation_points)
            all_short_operation_points.extend(short_operation_points)
        return all_long_operation_points, all_short_operation_points

    def _add_to_session(self):
        session.add_all(self.all_long_operation_points)
        session.add_all(self.all_short_operation_points)

    @staticmethod
    @log_on_end("Committed")
    def _commit() -> None:
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
