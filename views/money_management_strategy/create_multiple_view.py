from __future__ import annotations

from typing import Any

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from config.logging_config.log_decorators import log_on_end, log_on_start
from database import session
from database.models import MoneyManagementStrategy
from schemas.atr_schema import AtrSchema
from utils.range_utils import InvalidRangeInputsError, frange


class MoneyManagementStrategyCreateMultipleView:
    SL_TP_STEP = 0.1
    INT_STEP = 1

    def __init__(
        self,
        type: str,  # noqa: A002
        tp_multiplier_range: tuple[float, float],
        sl_multiplier_range: tuple[float, float],
        atr_parameter_range: tuple[int, int],
        risk_percentage_range: tuple[int, int],
    ):
        self.type: str = type
        self.tp_multiplier_range: tuple[float, float] = tp_multiplier_range
        self.sl_multiplier_range: tuple[float, float] = sl_multiplier_range
        self.atr_parameter_range: tuple[int, int] = atr_parameter_range
        self.risk_percentage_range: tuple[int, int] = risk_percentage_range

    @log_on_end("Finished MoneyManagementStrategyCreateMultipleView")
    def run(self) -> None:
        tp_values = self._get_tp_values()
        sl_values = self._get_sl_values()
        atr_values = self._get_atr_values()
        risk_values = self._get_risk_percentage_values()
        atr_schemas_data = self._get_atr_schemas_data(
            risk_values=risk_values,
            tp_values=tp_values,
            sl_values=sl_values,
            atr_values=atr_values,
        )
        atr_schemas = self._get_atr_schemas(atr_schemas_data=atr_schemas_data)
        self._create_money_management_strategies(atr_schemas=atr_schemas)
        self._commit()

    def _get_tp_values(self) -> list[float]:
        try:
            tp_values = list(
                frange(
                    self.tp_multiplier_range[0],
                    self.tp_multiplier_range[1] + self.SL_TP_STEP,
                    self.SL_TP_STEP,
                )
            )
        except InvalidRangeInputsError:
            raise

        return tp_values

    def _get_sl_values(self) -> list[float]:
        try:
            sl_values = list(
                frange(
                    self.sl_multiplier_range[0],
                    self.sl_multiplier_range[1] + self.SL_TP_STEP,
                    self.SL_TP_STEP,
                )
            )
        except InvalidRangeInputsError:
            raise

        return sl_values

    def _get_atr_values(self) -> list[int]:
        if self.atr_parameter_range[0] <= 0 or self.atr_parameter_range[1] <= 0:
            err = "Parameters must be positive integers"
            raise InvalidRangeInputsError(err)

        return list(
            range(
                self.atr_parameter_range[0],
                self.atr_parameter_range[1] + self.INT_STEP,
                self.INT_STEP,
            )
        )

    def _get_risk_percentage_values(self) -> list[float]:
        if self.risk_percentage_range[0] <= 0 or self.risk_percentage_range[1] <= 0:
            err = "Risk Percentages must be positive integers"
            raise InvalidRangeInputsError(err)

        return [
            i / 100
            for i in range(
                self.risk_percentage_range[0],
                self.risk_percentage_range[1] + self.INT_STEP,
                self.INT_STEP,
            )
        ]

    def _get_atr_schemas_data(
        self,
        risk_values: list[float],
        tp_values: list[float],
        sl_values: list[float],
        atr_values: list[int],
    ) -> list[dict[str, Any]]:
        atr_schemas_data = []
        for risk_value in risk_values:
            for tp_value in list(tp_values):
                for sl_value in list(sl_values):
                    for atr_value in list(atr_values):
                        atr_schemas_data.append(  # noqa: PERF401
                            {
                                "type": self.type,
                                "tp_multiplier": tp_value,
                                "sl_multiplier": sl_value,
                                "parameters": {"atr_parameter": atr_value},
                                "risk": risk_value,
                            }
                        )
        return atr_schemas_data

    @staticmethod
    def _get_atr_schemas(atr_schemas_data: list[dict[str, Any]]) -> list[AtrSchema]:
        atr_schemas = []
        for atr_schema_data in atr_schemas_data:
            try:
                atr_schema = AtrSchema(**atr_schema_data)
            except ValidationError:
                raise

            atr_schemas.append(atr_schema)
        return atr_schemas

    @staticmethod
    @log_on_start("Creating MoneyManagementStrategy")
    def _create_money_management_strategies(atr_schemas: list[AtrSchema]) -> None:
        for atr_schema in atr_schemas:
            money_management_strategy = MoneyManagementStrategy(**atr_schema.model_dump())  # type: ignore[union-attr]
            session.add(money_management_strategy)

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
