from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from config.logging_config.log_decorators import log_on_end

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from database.models import (
        Indicator,
        MoneyManagementStrategy,
        RawPointD1,
        ResampledPointD1,
        Strategy,
    )
    from models.operation_point import OperationPoints


class DatabaseHandler:
    def __init__(self, session: Session):
        self._session = session

    def commit_money_management_strategies(
        self,
        money_management_strategies: list[MoneyManagementStrategy],
    ) -> None:
        self._session.add_all(money_management_strategies)
        self._commit()

    def commit_operation_points(self, operation_points: OperationPoints) -> None:
        self._session.add_all(
            operation_points.long_operation_points
            + operation_points.short_operation_points
        )
        self._commit()

    def commit_raw_points(self, raw_points_d1: list[RawPointD1]) -> None:
        self._session.add_all(raw_points_d1)
        self._commit()

    def commit_resampled_points(
        self,
        resampled_points: list[ResampledPointD1],
    ) -> None:
        self._session.add_all(resampled_points)
        self._commit()

    def commit_strategies(
        self,
        strategies: list[Strategy],
    ) -> None:
        self._session.add_all(strategies)
        self._commit()

    def delete_money_management_strategies(
        self,
        money_management_strategies: list[MoneyManagementStrategy],
    ) -> None:
        for money_management_strategy in money_management_strategies:
            self._session.delete(money_management_strategy)
        self._commit()

    def delete_indicators(self, indicators: list[Indicator]) -> None:
        for indicator in indicators:
            self._session.delete(indicator)
        self._commit()

    @log_on_end("Committed")
    def _commit(self) -> None:
        try:
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise
        except IntegrityError:
            self._session.rollback()
            raise
        finally:
            self._session.close()
