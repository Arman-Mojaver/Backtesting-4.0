from config import config
from database.models import MoneyManagementStrategy, ResampledPointD1
from exceptions import (
    LargeAtrParameterError,
    NoMoneyManagementStrategiesError,
    NoResampledPointsError,
)
from schemas.instruments_schema import EnabledInstrumentsMismatchError


class OperationPointsCreateMultipleView:
    def __init__(self):
        self.resampled_points = ResampledPointD1.query.all()
        self.money_management_strategy = MoneyManagementStrategy.query.all()

    def run(self) -> None:
        self._validate_resampled_points_exist()
        self._validate_money_management_strategy_exists()
        self._validate_atr_parameter()
        self._validate_enabled_instruments()

    def _validate_resampled_points_exist(self):
        if not self.resampled_points:
            err = "No resampled points in db"
            raise NoResampledPointsError(err)

    def _validate_money_management_strategy_exists(self):
        if not self.money_management_strategy:
            err = "No money management strategies in db"
            raise NoMoneyManagementStrategiesError(err)

    def _validate_atr_parameter(self):
        atr_parameter = self.money_management_strategy[0].parameters["atr_parameter"]
        if len(self.resampled_points) < atr_parameter:
            err = (
                "Not enough resampled points for given atr_parameter"
                f"{len(self.resampled_points)=}, {atr_parameter=}"
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
