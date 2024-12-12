from __future__ import annotations

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from config.logging_config.log_decorators import log_on_end, log_on_start
from database import session
from database.models import MoneyManagementStrategy
from schemas.atr_schema import AtrSchema


class MoneyManagementStrategyCreateOneView:
    def __init__(
        self,
        type: str,  # noqa: A002
        tp_multiplier: float,
        sl_multiplier: float,
        parameters: dict[str, int],
    ):
        self.type: str = type
        self.tp_multiplier: float = tp_multiplier
        self.sl_multiplier: float = sl_multiplier
        self.parameters: dict[str, int] = parameters

        self.atr: AtrSchema | None = None

    @log_on_end("Finished MoneyManagementStrategyCreateOneView")
    def run(self) -> None:
        self._validate_atr_schema()
        self._create_money_management_strategy()
        self._commit()

    def _validate_atr_schema(self):
        try:
            self.atr = AtrSchema(
                type=self.type,
                tp_multiplier=self.tp_multiplier,
                sl_multiplier=self.sl_multiplier,
                parameters=self.parameters,
            )
        except ValidationError:
            raise

    @log_on_start("Creating MoneyManagementStrategy")
    def _create_money_management_strategy(self) -> None:
        money_management_strategy = MoneyManagementStrategy(**self.atr.model_dump())  # type: ignore[union-attr]
        session.add(money_management_strategy)

    @staticmethod
    @log_on_end("Committed")
    def _commit() -> None:
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
        finally:
            session.close()
